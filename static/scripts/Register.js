var checkbox=document.querySelector("#checkbox_id")
var registerButton=document.querySelector(".register-btn")



checkbox.addEventListener("change",()=>{
    let isChecked=checkbox.checked
    if(isChecked==true){
        registerButton.classList.remove("btn-secondary")
        registerButton.classList.remove("disabled")
        registerButton.classList.add("btn-primary")
    }else{
        registerButton.classList.add("btn-secondary")
        registerButton.classList.add("diabled")
    }
    
})
function show_password() {
    var password1 = document.getElementsByName("password1")[0];
    var password2 = document.getElementsByName("password2")[0];
    if (password1.type === "password") {
      password1.type = "text";
      password2.type = "text";
    } else {
      password1.type = "password";
      password2.type = "password";
    }
  }
function submit_action(){
    var passw = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    var password1 = String(document.getElementsByName("password1")[0].value)
    var password2 = String(document.getElementsByName("password2")[0].value)
    if (password1==password2)
        {
            try{
                console.log(password1+"   "+password2)
                if (passw.test(password1)) 
            {
                console.log("Good ")
                return false
            }
            else
            {

            alert("Passwords did not meet criteria:\n 1.Minimum of 8 characters \n 2.One Special Character \n 3.One Digit \n 4.One Capital Letter ")
            return false
            }

            }
            catch(e){
                console.log(e)
            }
            
          
        }
    else
    alert("Passwords did not match!! ")
    return false
}

