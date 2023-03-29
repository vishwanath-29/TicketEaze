from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()

# Helper Table for User Bookings
userbooking = db.Table('userbooking',
    db.Column('booking_id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('show_id', db.Integer, db.ForeignKey('show.id'))
)
 
# Helper Table for Shows in Venue
showinvenue = db.Table('shows',
    db.Column('id', db.Integer,primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True)
)
# Show Model
class show(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   rating = db.Column(db.Integer)  
   tags = db.Column(db.String(200))
   price = db.Column(db.Float)

   def __init__(self, name, rating, tags ,price):
    self.name = name
    self.rating = rating
    self.tags = tags
    self.price = price


# User Model
class user(UserMixin,db.Model):
   id = db.Column( db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100))
   phonenumber = db.Column(db.String(12))  
   dateofbirth = db.Column(db.Date)
   password = db.Column(db.String(257))
   bookings = db.relationship('show',secondary=userbooking, backref='bookings')

   def __init__(self, name,email,phonenumber,dateofbirth,password):
    self.name = name
    self.email =email
    self.phonenumber = phonenumber
    self.dateofbirth = dateofbirth
    self.password = password
    

# Venue Model
class venue(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   capacity = db.Column(db.String(200))
   pincode = db.Column(db.String(10))
   venuetype = db.Column(db.String(10))
   showshosted = db.relationship('show',secondary=showinvenue, backref='showshosted')

   def __init__(self, name, city, capacity ,pincode):
    self.name = name
    self.city = city
    self.capacity = capacity
    self.pincode = pincode



