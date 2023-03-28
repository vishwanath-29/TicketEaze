from flask import Flask, render_template , request , redirect
from flask_login import UserMixin,login_user,LoginManager,current_user,logout_user,login_required
from flask_migrate import Migrate

from models import *
import hashlib,datetime

# Intialization and Configs 
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketeaze.db'
app.config['SECRET_KEY'] = 'secret-key'
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

@app.before_first_request  
def create_tables():
    db.create_all()

#Home page and Route 
@app.route("/")
def hello():
  return render_template('Home/Home.html')

@app.route("/login/user",methods=['GET','POST'])
def user_login():
  if request.method=='POST':
    print("Hello")
  else:
     return render_template("Register/UserLogin.html")

 

@app.route("/login/admin")
def admin_login():
  return render_template("Register/AdminLogin.html")

#Register Route and Method
@app.route("/register",methods=['GET','POST'])
def register():
  if request.method=='POST':
    name=request.form.get("name")
    email=request.form.get("email")
    dateofbirth=request.form.get("dateofbirth")
    dateofbirth=datetime.datetime.strptime(dateofbirth, "%Y-%m-%d").date()
    phonenumber=request.form.get("phonenumber")
    password=request.form.get("password1")
    password=hashlib.sha256(password.encode()).hexdigest()
    if user.query.filter_by(email=email).first():
      return render_template("Register/Register.html",status=1)  
    else:
      user_details = user(name=name, email=email,dateofbirth=dateofbirth,phonenumber=phonenumber,password=password)
      db.session.add(user_details)
      db.session.commit()  
      return redirect("/")
  else:
    return render_template("Register/Register.html")
  
@app.route("/management")
def management():
  return render_template("Admin/Management.html")

  
@app.route("/management/venue")
def managevenue():
  return render_template("Admin/ManageVenue.html")

  
@app.route("/management/event")
def manageevent():
  return render_template("Admin/ManageEvent.html")

  
@app.route("/management/event/add")
def addevent():
  return render_template("Admin/AddEvent.html")

@app.route("/management/venue/add")
def addvenue():
  return render_template("Admin/AddVenue.html")

if __name__ == "__main__":
  app.run(debug=True)

