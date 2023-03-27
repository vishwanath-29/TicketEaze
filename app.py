from flask import Flask, render_template , request , redirect
from models import user,venue,show,userbooking,showinvenue,db

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketeaze.db'

db.init_app(app)

@app.before_first_request  
def create_tables():
    db.create_all()

#Home page and Route 
@app.route("/")
def hello():

  student = students(name='Vishwanath', city='Chennai',addr='Chennai',pin= '600064')
  print(student)
  print(db)
  db.session.add(student)
  db.session.commit()
  users = students.query.all()
  
  for i in users:
    print(i.name)
   
  return render_template('Home/Home.html')

#Register Route and Method
@app.route("/register",methods=['GET','POST'])
def register():
  if request.method=='POST':
    print(request.form.get("name"))
    print(request.form.get("email"))
    print(request.form.get("dateofbirth"))
    print(request.form.get("password1"))   
    return redirect("/")
  else:
    return render_template("Register/Register.html")
  
@app.route("/management")
def admin_view():
  return render_template("Admin/Management.html")


if __name__ == "__main__":
  app.run(debug=True)

