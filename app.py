from flask import Flask, render_template , request , redirect ,session ,flash,url_for
from flask_login import login_user,LoginManager,current_user,logout_user,login_required
from flask_migrate import Migrate
from flask_session import Session
from werkzeug.utils import secure_filename

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
  if request.method == 'POST':
        f = request.files['venue_img']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
  return render_template('Home/Home.html')

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
      return render_template("Register/Register.html",status=1)  
    else:
      user_details = user(name=name, email=email,dateofbirth=dateofbirth,phonenumber=phonenumber,password=password)
      db.session.add(user_details)
      db.session.commit()  
      return redirect("/")
  else:
    return render_template("Register/Register.html")

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
     return render_template("Register/UserLogin.html")

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
  return render_template("Register/AdminLogin.html")

# Logout user
@app.route('/logout')
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']
    # Flashing the message to template for alerting the success of logging out
    flash('Have successfully logged out 👍!')
    return redirect('/')


@app.route("/management")
@admin_login_required
def management():
  return render_template("Admin/Management.html")

  
@app.route("/management/venue")
@admin_login_required
def managevenue():
  return render_template("Admin/ManageVenue.html")

  
@app.route("/management/event")
@admin_login_required
@login_required
def manageevent():
  return render_template("Admin/ManageEvent.html")

  
@app.route("/management/event/add",methods=['GET','POST'])
@admin_login_required
def addevent():
  if(request.method=="POST"):
     event_name=request.form.get("event_name")
     event_desc=request.form.get("event_desc")
     tags=request.form.get("event_tags")
     event_location=request.form.get("event_loc")
     event_venue=request.form.get("event_venue")
     event_img=request.files["event_img"]
     filename = secure_filename(f.filename)
     ticket_price=request.form.get("event_price")
     event_capacity=request.form.get("event_capacity")

     print(event_name)
     print(event_desc)
     print(event_location)

  return render_template("Admin/AddEvent.html")

@app.route("/management/venue/add",methods=['GET','POST'])
@admin_login_required
def addvenue():

  if request.method=='POST':
     venue_name=request.form.get("venue_name")
     venue_capacity=request.form.get("venue_capacity")
     venue_pincode=request.form.get("venue_pincode")
     venue_type=request.form.get("venue_type")
     venue_location=request.form.get("venue_location")
     
     venue_img = request.files['venue_img']
    
     extension = os.path.splitext(venue_img.filename)[1]
  

     venue_details = venue(name=venue_name,venuetype=venue_type,city=venue_location,capacity=venue_capacity,pincode=venue_pincode)
     db.session.add(venue_details)
     db.session.commit() 
     venue_details = db.session.query(venue).filter_by(name=venue_name).first()
     filename=str(venue_details.id)+extension
     venue_img.save(os.path.join(app.config['UPLOAD_FOLDER'],"venue", filename)) 
  return render_template("Admin/AddVenue.html")

@app.route("/management/event/edit")
@admin_login_required
def editevent():
  return render_template("Admin/EditEvent.html")

@app.route("/management/venue/edit")
@admin_login_required
def editvenue():
  return render_template("Admin/EditVenue.html")

@app.route("/management/event/remove")
@admin_login_required
def removeevent():
   return render_template("Admin/RemoveEvent.html")

@app.route("/management/venue/remove")
@admin_login_required
def removevenue():
   return render_template("Admin/RemoveVenue.html")



if __name__ == "__main__":
  app.run(debug=True)


    





