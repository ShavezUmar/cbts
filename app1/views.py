from django.shortcuts import render,redirect
#from django.http import HttpResponse
from .models import users,museums,bookings
from django.contrib import messages
from .botresponse import botresponse_mainc,botresponse_explore,botresponse_buyrefundticks
from random import randint
# Create your views here.
chat_history = []

def genran(ids):
    idsl=[doc["bid"] for doc in ids if "bid" in doc]
    ran=randint(300,399)
    while ran in idsl:
        ran=randint(300,399)
    return ran

def test(request):
    return render(request,'test.html')

def login1(request):
    if request.method=="POST":
        uname = request.POST.get("uname")
        password = request.POST.get("password")
        user = users.find_one({"username":uname})
        
        if user and user["password"] == password:
                return redirect("mainc")
        else:
            messages.error(request,"Incorrect Username/Password")
    global chat_history
    chat_history = []
    return render(request,'login1.html')

def mainc(request):
    user = users.find_one({"uid":101})
    museums1 = list(museums.find())
    bookings1 = list(bookings.find({"uid":101}))
    tickets_booked = sum(booking["tickets_booked"] for booking in bookings1)
    for booking in bookings1:
        museum = museums.find_one({"mid":booking["mid"]})
        booking["mname"] = museum["mname"] if museum else "Unknown Museum"
        booking["museum_img"] = museum["image"] if museum else "IMG"

    global chat_history
    if request.method == "POST":
        user_message = request.POST.get('user_message')
        chat_history.append({"sender":"user","text":user_message})

        chatbot_response,redirecting = botresponse_mainc(user_message)
        chat_history.append({"sender":"bot","text":chatbot_response})

        if redirecting:
            if redirecting == "explore":
                return redirect('explore')
            elif redirecting == "buyrefundticks":
                return redirect('buyrefundticks')
            elif redirecting == "payment":
                return redirect('payment')
        

    context = {
        'user' : user,
        'tickets_booked' : tickets_booked,
        'bookings' : bookings1,
        'museums' : museums1,
        'messages' : chat_history
    }
    return render(request,'mainc.html',context)

def explore(request):
    user = users.find_one({"uid":101})
    museums1 = list(museums.find())
    bookings1 = list(bookings.find({"uid":101}))
    tickets_booked = sum(booking["tickets_booked"] for booking in bookings1)
    slots_remaining = sum(museum["ticket_slots"][i]["remaining"] for i in range(2) for museum in museums1)

    global chat_history
    if request.method == "POST":
        user_message = request.POST.get('user_message')
        chat_history.append({"sender":"user","text":user_message})

        chatbot_response,redirecting = botresponse_explore(user_message)
        chat_history.append({"sender":"bot","text":chatbot_response})

        if redirecting:
            if redirecting == "mainc":
                return redirect('mainc')
            elif redirecting == "buyrefundticks":
                return redirect('buyrefundticks')
            elif redirecting == "payment":
                return redirect('payment')
        

    context = {
        'user' : user,
        'tickets_booked' : tickets_booked,
        'bookings' : bookings1,
        'museums' : museums1,
        'messages' : chat_history,
        'slots_remaining' : slots_remaining
    }
    return render(request,'explore.html',context)

def buyrefundticks(request):
    user = users.find_one({"uid":101})
    museums1 = list(museums.find())
    bookings1 = list(bookings.find({"uid":101}))
    tickets_booked = sum(booking["tickets_booked"] for booking in bookings1)
    
    global chat_history
    if request.method == "POST":
        form_id = request.POST.get('form_id')
        if form_id == "R":
            print("RRRRRRRRRRRR")
            user_message = request.POST.get('user_message')
            chat_history.append({"sender":"user","text":user_message})

            chatbot_response,redirecting = botresponse_buyrefundticks(user_message)
            chat_history.append({"sender":"bot","text":chatbot_response})

            if redirecting:
                if redirecting == "explore":
                    return redirect('explore')
                elif redirecting == "mainc":
                    return redirect('mainc')
                elif redirecting == "payment":
                    return redirect('payment')
        
        if form_id == "L":
            print("LLLLLLLLLLLL")
            action = request.POST.get('action')  # Get the action ("buy" or "refund")
            identifier = int(request.POST.get('museum_or_booking_id'))
            num_tickets = int(request.POST.get('num_tickets', 0))
            booking_date = request.POST.get('booking_date')

            if action == "buy":
                museum = museums.find_one({"mid":identifier})
                if museum:
                    ticket_slot = next(
                        (slot for slot in museum['ticket_slots'] if slot['date'] == booking_date), None
                    )
                    if ticket_slot and ticket_slot['remaining'] >= num_tickets:
                        total_price = num_tickets * museum['ticket_price']
                        user = users.find_one({"uid": 101})
                        if user['balance'] >= total_price:
                            users.update_one({"uid": 101}, {"$inc": {"balance": -total_price}})
                            museums.update_one({"mid": identifier, "ticket_slots.date": booking_date}, {"$inc": {"ticket_slots.$.remaining": -num_tickets}})
                            ids = list(bookings.find({},{"_id":0,"bid":1}))
                            bookings.insert_one({
                                "bid": genran(ids),
                                "uid": 101,
                                "mid": identifier,
                                "booking_date": booking_date,
                                "tickets_booked": num_tickets,
                                "total_price": total_price,
                                "payment_status": "Paid"
                            })
                            chatbot_response = "Tickets bought successfully!"
                            chat_history.append({"sender":"bot","text":chatbot_response})
                        else:
                            chatbot_response = "Insufficient balance."
                            chat_history.append({"sender":"bot","text":chatbot_response})
                    else:
                        chatbot_response = "Not enough tickets available on this date."
                        chat_history.append({"sender":"bot","text":chatbot_response})
                else:
                    chatbot_response = "Invalid Museum ID."
                    chat_history.append({"sender":"bot","text":chatbot_response})
            
            elif action == "refund":
                booking = bookings.find_one({"bid": identifier})
                if booking and booking['booking_date'] == booking_date:
                    if booking['tickets_booked'] >= num_tickets:
                        refund_amount = num_tickets * museums.find_one({"mid": booking['mid']})['ticket_price']
                        users.update_one({"uid": 101}, {"$inc": {"balance": refund_amount}})
                        museums.update_one({"mid": booking['mid'], "ticket_slots.date": booking_date}, {"$inc": {"ticket_slots.$.remaining": num_tickets}})
                        new_ticket_count = booking['tickets_booked'] - num_tickets
                        if new_ticket_count>0:
                            bookings.update_one({"bid":identifier}, {"$inc": {"tickets_booked": -num_tickets}})
                        else:
                            bookings.delete_one({"bid":identifier})
                        chatbot_response = "Tickets refunded successfully!"
                        chat_history.append({"sender":"bot","text":chatbot_response})
                    else:
                        chatbot_response = "You can't refund more tickets than you booked."
                        chat_history.append({"sender":"bot","text":chatbot_response})
                else:
                    chatbot_response = "Invalid Booking ID or Date."
                    chat_history.append({"sender":"bot","text":chatbot_response})

    context = {
        'user' : user,
        'tickets_booked' : tickets_booked,
        'bookings' : bookings1,
        'museums' : museums1,
        'messages' : chat_history
    }
    return render(request,'buyrefundticks.html',context)

def payment(request):
    user = users.find_one({"uid":101})
    museums1 = list(museums.find())
    bookings1 = list(bookings.find({"uid":101}))
    tickets_booked = sum(booking["tickets_booked"] for booking in bookings1)
    
    global chat_history
    if request.method == "POST":
        form_id = request.POST.get('form_id')
        if form_id == "R":
            print("RRRRRRRRRRRR")
            user_message = request.POST.get('user_message')
            chat_history.append({"sender":"user","text":user_message})

            chatbot_response,redirecting = botresponse_buyrefundticks(user_message)
            chat_history.append({"sender":"bot","text":chatbot_response})

            if redirecting:
                if redirecting == "explore":
                    return redirect('explore')
                elif redirecting == "mainc":
                    return redirect('mainc')
                elif redirecting == "payment":
                    return redirect('payment')
        
        if form_id == "L":
            card_type = request.POST.get('card_type')
            card_number = request.POST.get('card_number')
            exp_date = request.POST.get('exp_date')
            card_cvv = request.POST.get('card_cvv')
            amount = int(request.POST.get('amount'))

            user = users.find_one({"uid":101})

            users.update_one({"uid": 101}, {"$inc": {"balance": amount}})
            chatbot_response = f"₹{amount} added to your balance!"
            chat_history.append({"sender":"bot","text":chatbot_response})

    context = {
        'user' : user,
        'tickets_booked' : tickets_booked,
        'bookings' : bookings1,
        'museums' : museums1,
        'messages' : chat_history
    }
    return render(request,'payment.html',context)