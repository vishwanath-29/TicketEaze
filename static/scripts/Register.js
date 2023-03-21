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

