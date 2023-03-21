from flask import Flask, render_template , request , redirect
app = Flask(__name__)

#Home page and Route 
@app.route("/")
def hello():
  return render_template('Home/Home.html')

#Register Route and Method
@app.route("/register",methods=['GET','POST'])
def register():
  if request.method=='POST':
    return redirect("/")
  else:
    return render_template("Register/Register.html")
if __name__ == "__main__":
  app.run()
