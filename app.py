from flask import Flask, render_template , request , redirect
from models import user,venue,show,userbooking,showinvenue,db
import hashlib

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketeaze.db'

db.init_app(app)

@app.before_first_request  
def create_tables():
    db.metadata.clear()
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
    password=request.form.get("password1")
    password=hashlib.sha256(password.encode()).hexdigest()
    print(name+email+dateofbirth+password)
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

