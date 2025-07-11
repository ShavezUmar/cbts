from django.db import models
from db_connection import db
# Create your models here.
users = db['Users']
museums = db['Museums']
bookings = db['Bookings']