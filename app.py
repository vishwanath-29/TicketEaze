from flask import Flask, render_template , request , redirect ,session ,flash,url_for
from flask_login import login_user,LoginManager,current_user,logout_user,login_required
from flask_migrate import Migrate
from flask_session import Session
from werkzeug.utils import secure_filename
from sqlalchemy import delete,select,insert

from models import *
from datetime import timedelta
import hashlib,datetime
import os
import os.path

# Intialization and Configs 
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketeaze.db'
app.config['SECRET_KEY'] = 'secret-key'

# Server Side Sessions
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# File Uploads Configs 
UPLOAD_FOLDER = './static/file_uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Login Manager Configs
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)
db.init_app(app)

# Load user based of current user type 
@login_manager.user_loader
def load_user(user_id):
        if session['user_type']=='user':
          record = user.query.get(int(user_id))
        elif session['user_type']=='admin':
          record = admin.query.get(int(user_id))
        return record

# Before First Request Logging out users and 
@app.before_first_request  
def init():
    db.create_all()
    session.clear()
    logout_user()
    

# Home page and Route 
@app.route("/",methods=['GET','POST'])
def home():
  events = db.session.query(show).all() 
  return render_template('Home/Home.html',events=events,title="Home")

# Register Route and Method
@app.route("/register",methods=['GET','POST'])
def register():
  if request.method=='POST':
    name=request.form.get("name")
    email=request.form.get("email")
    dateofbirth=request.form.get("dateofbirth")
    dateofbirth=datetime.datetime.strptime(dateofbirth, "%Y-%m-%d").date()
    phonenumber=request.form.get("phonenumber")
    password=request.form.get("password1")
    # Hashing password in SHA256
    password=hashlib.sha256(password.encode()).hexdigest()
    # Check if email already exist
    if user.query.filter_by(email=email).first():
      return render_template("Register/Register.html",status=1,title="Register")  
    else:
      user_details = user(name=name, email=email,dateofbirth=dateofbirth,phonenumber=phonenumber,password=password)
      db.session.add(user_details)
      db.session.commit()  
      return redirect("/")
  else:
    return render_template("Register/Register.html",title="Register")

# User logging
@app.route("/login/user",methods=['GET','POST'])
def user_login():
  if request.method=='POST':
    email=request.form.get("email")
    password=request.form.get("password")
    password=hashlib.sha256(password.encode()).hexdigest()
    user_login = user.query.filter_by(email=email).first()
    
    if user_login:
            if(user_login.password==password):
                # Setting the current session user type as user for logging in 
                session['user_type'] = 'user'
                login_user(user_login) 
                return redirect("/")  
            else:
               flash('Invalid Credentials!')
               return redirect("/login/user")      
  else:
     return render_template("Register/UserLogin.html",title="User Login")

# Admin Login
@app.route("/login/admin",methods=['GET','POST'])
def admin_login():
  if request.method=='POST':
    email=request.form.get("email")
    password=request.form.get("password")
    password=hashlib.sha256(password.encode()).hexdigest()
    admin_login = db.session.query(admin).filter_by(email=email).first()
    if admin_login:
            if(admin_login.password==password):
                # Setting the user type as admin for logging in
                session['user_type'] = 'admin'
                login_user(admin_login) 
                return redirect("/management")
            else:
               flash('Invalid Credentials!')
               return redirect("/login/admin")
  return render_template("Register/AdminLogin.html",title="Admin Login")

# Logout user
@app.route('/logout')
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']
    # Flashing the message to template for alerting the success of logging out
    flash('Have successfully logged out 👍!')
    return redirect('/')

# Management Home
@app.route("/management")
@admin_login_required
def management():
  return render_template("Admin/Management.html",title="Management")

# Management of Venue Home 
@app.route("/management/venue")
@admin_login_required
def managevenue():
  return render_template("Admin/ManageVenue.html",title="Venue Management")

# Management of Event Home
@app.route("/management/event")
@admin_login_required
@login_required
def manageevent():
  return render_template("Admin/ManageEvent.html",title="Manage Event")

# Addition of Event
@app.route("/management/event/add",methods=['GET','POST'])
@admin_login_required
def addevent():
  if(request.method=="POST"):
     # Getting Values from Form
     event_name=request.form.get("event_name")
     event_desc=request.form.get("event_desc")
     tags=request.form.get("event_tags")
     event_venue=request.form.get("event_venue")
     event_price=request.form.get("event_price")
     event_capacity=request.form.get("event_capacity")
     event_short_desc=request.form.get("event_short_desc")
     # Getting Event Location based of Venue Selected 
     event_location=db.session.query(venue).filter_by(id=event_venue).first().city
     # Creating DB Object
     event_details = show(name=event_name,description=event_desc,location=event_location,capacity=event_capacity,price=event_price,tags=tags,shortdescription=event_short_desc)
     # Adding value to Helper table by getting venue id and appending
     venue_details=db.session.query(venue).filter_by(id=event_venue).first()
     event_details.showshosted.append(venue_details)
     db.session.add(event_details)
     db.session.commit() 
     db.session.flush() 
     # Handling Event image
     event_img = request.files['event_img']
     extension = os.path.splitext(event_img.filename)[1]
     filename=str(event_details.id)+extension
     event_img.save(os.path.join(app.config['UPLOAD_FOLDER'],"event", filename)) 
  venues = db.session.query(venue).all()
  return render_template("Admin/AddEvent.html",venues=venues,title="Event Management")

# Venue Addition
@app.route("/management/venue/add",methods=['GET','POST'])
@admin_login_required
def addvenue():
  if request.method=='POST':
     # Getting Venue Details from Form
     venue_name=request.form.get("venue_name")
     venue_capacity=request.form.get("venue_capacity")
     venue_pincode=request.form.get("venue_pincode")
     venue_type=request.form.get("venue_type")
     venue_location=request.form.get("venue_location")
     # Creating DB Object
     venue_details = venue(name=venue_name,venuetype=venue_type,city=venue_location,capacity=venue_capacity,pincode=venue_pincode)
     db.session.add(venue_details)
     db.session.commit() 
     # Handling Image for venue
     venue_img = request.files['venue_img']
     extension = os.path.splitext(venue_img.filename)[1]
     venue_details = db.session.query(venue).filter_by(name=venue_name).first()
     filename=str(venue_details.id)+extension
     venue_img.save(os.path.join(app.config['UPLOAD_FOLDER'],"venue", filename)) 
  return render_template("Admin/AddVenue.html",title="Venue Management")

@app.route("/management/event/remove",methods=['GET','POST'])
@admin_login_required
def removeevent():
   if request.method=='POST':
      # Getting Event Id from request
      event_id=request.form.get('event_id')
      # Deleting the Event based of ID
      show.query.filter_by(id=event_id).delete()
      # Deleting Values in Helper Table and Shows in Venue
      d = delete(showinvenue).where(showinvenue.c.show_id == event_id)
      db.session.execute(d)
      db.session.commit()
      # Getting the new Events List
      events = db.session.query(show).all()
      message="Have successfully Deleted 👍!"
      # Sending Message and re-rendering
      return render_template("Admin/RemoveEvent.html",events=events,message=message,title="Event Management")
   events = db.session.query(show).all()
   return render_template("Admin/RemoveEvent.html",events=events,title="Event Management")

# Deletion of Venue
@app.route("/management/venue/remove",methods=['GET','POST'])
@admin_login_required
def removevenue():
   if request.method=='POST':
      # Getting Venue Id from request
      venue_id=request.form.get('venue_id')
      # Deleting the Venue based of ID
      venue.query.filter_by(id=venue_id).delete()
      # Deleting Values in Helper Table and Shows in Venue
      # Getting Show ids in that Venue
      show_id=select(showinvenue.c.show_id).where(showinvenue.c.venue_id == venue_id)
      show_id=db.session.execute(show_id)
      show_id=[id for id, in show_id]
      # Deleting Shows in that Venue
      for i in show_id:
         show.query.filter_by(id=i).delete()
      # Deleting the Row of venue_id in Showinvenue
      d = delete(showinvenue).where(showinvenue.c.venue_id == venue_id)
      db.session.execute(d)
      db.session.commit()
      # Getting the new Venues List
      venues = db.session.query(venue).all()
      message="Have successfully Deleted 👍!"
      # Sending Message and re-rendering
      return render_template("Admin/RemoveVenue.html",venues=venues,message=message,title="Venue Management")
   venues = db.session.query(venue).all()
   return render_template("Admin/RemoveVenue.html",venues=venues,title="Venue Management")


@app.route("/management/event/edit")
@admin_login_required
def editevent():
  return render_template("Admin/EditEvent.html",title="Event Management")

@app.route("/management/venue/edit")
@admin_login_required
def editvenue():
  return render_template("Admin/EditVenue.html",title="Venue Management")


# Ticket Booking Functionality 
@app.route("/event/booktickets/<int:event_id>",methods=['GET','POST'])
def ticket_booking(event_id):
   # User not authenticated redirect to login
   if not current_user.is_authenticated:
      return redirect("/login/user")
   if request.method=='POST':
      # Get the number of tickets from webpage
      numberoftickets=request.form.get('ticketcount')
      # Get Current user details
      user_details=current_user
      # Get Event Details based of ID
      event_details = db.session.query(show).filter_by(id=event_id).first()
      # Update the current capacity with number of tickets sold
      event_details.currentcapacity-=int(numberoftickets)
      # Total Cost
      total_cost=event_details.price*int(numberoftickets)
      # Insert the booking into booking helper table
      booking_query = insert(userbooking).values(user_id=user_details.id,show_id=event_id,ticket_count=numberoftickets,total_price=total_cost)
      db.session.execute(booking_query)
      db.session.commit()
   event_details = db.session.query(show).filter_by(id=event_id).first()
   return render_template("Events/EventPage.html",event_details=event_details,title="Ticket Booking")


@app.route("/management/event/list")
@admin_login_required
def eventlist():
   return render_template("Admin/EventList.html",title="Event List")

@app.route('/management/venue/list')
@admin_login_required
def venuelist():
   return render_template("Admin/VenueList.html",title="Venue List")




# @app.route("/orders",methods=['GET','POST'])
# @login_required
# def myorders():
#    userid=current_user.id
#    bookings=select(userbooking.c.booking_id,userbooking.c.show_id,userbooking.c.ticket_count,userbooking.c.total_price).where(userbooking.c.user_id == userid)
   
#    bookings=db.session.execute(bookings)
#    show_id=[]
#    bookings=list(bookings)
   
#    for i in range (len(bookings)):
#       show_id.append(bookings[i][1]) 
#    show_details=db.session.query(show).filter(show.id.in_(show_id))
#    show_details_dict={}
#    for i in show_details:
#       show_details_dict[i.id]=i
#    print(bookings)
#    return render_template("Orders/Orders.html",events=show_details_dict,bookings=bookings,numberofbookings=len(bookings))

@app.route("/myorders",methods=['GET','POST'])
@login_required
def myorders():
   
   if request.method=="POST":
      booking_id=request.form.get('booking_id')
      userid=current_user.id
      bookings=select(userbooking.c.show_id,userbooking.c.ticket_count,userbooking.c.total_price).where(userbooking.c.booking_id == booking_id)
      bookings=db.session.execute(bookings)
      bookings=list(bookings)
      show_id=bookings[0][0]
      show_details=db.session.query(show).filter_by(id=show_id).first()
      return render_template("Orders/Ticket.html",event=show_details,bookings=bookings,booking_id=booking_id)
   else:
    userid=current_user.id
    bookings=select(userbooking.c.booking_id,userbooking.c.show_id,userbooking.c.ticket_count,userbooking.c.total_price).where(userbooking.c.user_id == userid)
    bookings=db.session.execute(bookings)
    show_id=[]
    bookings=list(bookings)
    for i in range (len(bookings)):
          show_id.append(bookings[i][1]) 
    show_details=db.session.query(show).filter(show.id.in_(show_id))
    show_details_dict={}
    for i in show_details:
          show_details_dict[i.id]=i
    return render_template("Orders/OrdersPage.html",events=show_details_dict,bookings=bookings,numberofbookings=len(bookings))

@app.route("/myorders/tickets")
@login_required
def ticket_view():
   return render_template("Orders/Ticket.html",title="Ticket")
   
if __name__ == "__main__":
  app.run(debug=True)


    





