# AI Chatbot based Ticket Booking System for Museums
This is a Django-based web application for booking museum tickets through a chatbot interface. It uses MongoDB as the database and runs inside a Python virtual environment. The project includes sample data for testing.

### Features
- Chatbot interface for booking
- MongoDB-backed storage for users, tickets, and museums
- Django-based backend
- Sample database collections with test data

---
1. Clone the repository

   git clone https://github.com/ShavezUmar/cbts.git \
   cd cbts

2. Set up the virtual environment

   python -m venv env
   source env\Scripts\activate

3. Install dependencies

   pip install -r requirements.txt

4. Sample Database

   Sample data is provided under sample_data/ \
   mongoimport --db cbts --collection Bookings --file sample_data/Bookings.json --jsonArray \
   mongoimport --db cbts --collection Museums --file sample_data/Museums.json --jsonArray \
   mongoimport --db cbts --collection Users --file sample_data/Users.json --jsonArray

5. Run the Django server

   python manage.py runserver \
   Visit http://127.0.0.1:8000/app1/login1/ to interact with the chatbot.
---

## Project Structure
cbts/ \
  ├── app1/                      # App \
  ├── cbts/ \
  ├── sample_data/ \
  │   ├── Bookings.json \
  │   ├── Museums.json \
  │   └── Users.json \
  ├── static/ \
  ├── templates/ \
  ├── .gitignore \
  ├── db_connection.py \
  ├── manage.py \
  └── requirements.txt

## Tech Stack
- HTML, CSS (frontend)
- Django (backend)
- MongoDB (database)
