from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask import redirect ,session
from flask_login import current_user
from functools import wraps

db = SQLAlchemy()

# Helper Table for User Bookings
userbooking = db.Table('userbooking',
    db.Column('booking_id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('show_id', db.Integer, db.ForeignKey('show.id')),
    db.Column('ticket_count', db.Integer),
    db.Column('total_price',db.Float)
)
 
# Helper Table for Shows in Venue
showinvenue = db.Table('showinvenue',
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True)
)
# Show Model
class show(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   description = db.Column(db.String(100))
   shortdescription = db.Column(db.String(20))
   location = db.Column(db.String(100)) 
   capacity = db.Column(db.Integer)  
   tags = db.Column(db.String(200))
   price = db.Column(db.Float)
   rating = db.Column(db.Integer)
   currentcapacity = db.Column(db.Integer) 
   showshosted = db.relationship('venue',secondary=showinvenue, backref='showshosted')

   def __init__(self, name, description,location,capacity, tags ,price,shortdescription):
    self.name = name
    self.description = description
    self.location=location
    self.capacity=capacity
    self.tags = tags
    self.price = price
    self.currentcapacity=capacity
    self.shortdescription=shortdescription


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
   

   def __init__(self, name, city, capacity ,pincode,venuetype):
    self.name = name
    self.city = city
    self.capacity = capacity
    self.pincode = pincode
    self.venuetype = venuetype



# Admin Model
class admin(UserMixin,db.Model):
   id = db.Column( db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100))
   phonenumber = db.Column(db.String(12))  
   password = db.Column(db.String(257))

   def __init__(self, name,email,phonenumber,password):
    self.name = name
    self.email =email
    self.phonenumber = phonenumber
    self.password = password


def admin_login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not current_user.is_anonymous :
          if session['user_type']=='admin':
              return f(*args, **kwargs)
          else:
              return redirect("/")
        return redirect("/")
    return decorated_func
