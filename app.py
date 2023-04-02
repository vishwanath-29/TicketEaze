from flask import Flask, render_template , request , redirect ,session ,flash
from flask_login import UserMixin,login_user,LoginManager,current_user,logout_user,login_required
from flask_migrate import Migrate

from models import *
import hashlib,datetime

# Intialization and Configs 
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketeaze.db'
app.config['SECRET_KEY'] = 'secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = 0
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
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
        if session['user_type']=='user':
          record = user.query.get(int(user_id))
        elif session['user_type']=='admin':
          record = admin.query.get(int(user_id))
        return record


@app.before_first_request  
def init():
    logout_user()
    db.create_all()

#Home page and Route 
@app.route("/")
def hello():
  return render_template('Home/Home.html')

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

@app.route("/login/user",methods=['GET','POST'])
def user_login():
  if request.method=='POST':
    email=request.form.get("email")
    password=request.form.get("password")
    password=hashlib.sha256(password.encode()).hexdigest()
    user_login = user.query.filter_by(email=email).first()
    
    if user_login:
            if(user_login.password==password):
                session['user_type'] = 'user'
                login_user(user_login) 
                return redirect("/")        
  else:
     return render_template("Register/UserLogin.html")

@app.route("/login/admin",methods=['GET','POST'])
def admin_login():
  if request.method=='POST':
    email=request.form.get("email")
    password=request.form.get("password")
    password=hashlib.sha256(password.encode()).hexdigest()
    admin_login = db.session.query(admin).filter_by(email=email).first()
    if admin_login:
            if(admin_login.password==password):
                session['user_type'] = 'admin'
                login_user(admin_login) 
                return redirect("/management")
  return render_template("Register/AdminLogin.html")

 
@app.route('/logout')
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']
    flash('You have successfully logged yourself out.')
    return redirect('/')


@app.route("/management")
@login_required
def management():
  return render_template("Admin/Management.html")

  
@app.route("/management/venue")
def managevenue():
  return render_template("Admin/ManageVenue.html")

  
@app.route("/management/event")
@login_required
def manageevent():
  return render_template("Admin/ManageEvent.html")

  
@app.route("/management/event/add")
@login_required
def addevent():
  return render_template("Admin/AddEvent.html")

@app.route("/management/venue/add")
@login_required
def addvenue():
  return render_template("Admin/AddVenue.html")

if __name__ == "__main__":
  app.run(debug=True)


import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


