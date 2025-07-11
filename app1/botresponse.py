from .models import users,museums,bookings

def botresponse_mainc(user_message):
    user_message = user_message.lower()
    if user_message in ["hi", "hello"]:
        return "Hello! How can I assist you today?",0
    elif "what can you do" in user_message:
        return "I can help you buy/refund tickets or explore museums. Type 'buy tickets' or 'explore museums'.",0
    elif "how do i buy tickets" in user_message:
        return "Type 'buy tickets' to proceed.",0
    elif "how do i refund tickets" in user_message:
        return "Type 'refund tickets' to proceed.",0
    elif "buy tickets" in user_message or "refund tickets" in user_message:
        return "Redirecting to tickets page.","buyrefundticks"
    elif "explore museums" in user_message:
        return "Redirecting to explore page.","explore"
    elif "add balance" in user_message:
        return "Redirecting to payment page.","payment"
    elif "how do i add balance" in user_message:
        return "Type 'add balance' to add balance",0
    else:
        return "I'm sorry, I didn't understand that.",0
    
def botresponse_explore(user_message):
    user_message = user_message.lower()
    if user_message in ["hi", "hello"]:
        return "Hello! How can I assist you today?",0
    elif "what can you do" in user_message:
        return "Here, you can explore all the museums.",0
    elif "buy tickets" in user_message or "refund tickets" in user_message:
        return "Redirecting to tickets page.","buyrefundticks"
    elif "back" in user_message:
        return "Redirecting to main page.","mainc"
    elif "add balance" in user_message:
        return "Redirecting to payment page.","payment"
    elif "how do i add balance" in user_message:
        return "Type 'add balance' to add balance",0
    else:
        return "I'm sorry, I didn't understand that.",0

def botresponse_buyrefundticks(user_message):
    user_message = user_message.lower()
    if user_message in ["hi", "hello"]:
        return "Hello! How can I assist you today?",0
    elif "what can you do" in user_message:
        return "Here, you buy/refund tickets",0
    elif "explore museums" in user_message:
        return "Redirecting to explore page.","explore"
    elif "back" in user_message:
        return "Redirecting to main page.","mainc"
    elif "add balance" in user_message:
        return "Redirecting to payment page.","payment"
    elif "how do i add balance" in user_message:
        return "Type 'add balance' to add balance",0
    else:
        return "I'm sorry, I didn't understand that.",0
    
def botresponse_payment(user_message):
    user_message = user_message.lower()
    if user_message in ["hi", "hello"]:
        return "Hello! How can I assist you today?",0
    elif "what can you do" in user_message:
        return "Here, you can add balance using a card",0
    elif "explore museums" in user_message:
        return "Redirecting to explore page.","explore"
    elif "buy tickets" in user_message or "refund tickets" in user_message:
        return "Redirecting to tickets page.","buyrefundticks"
    elif "back" in user_message:
        return "Redirecting to main page.","mainc"
    else:
        return "I'm sorry, I didn't understand that.",0