var ticketIncrease = document.querySelector("#increment")
var ticketDecrease = document.querySelector("#decrement")
var bookButton = document.querySelector("#book-button")
var alertMessage=document.querySelector("#alert-msg")
var numberOfTickets = document.querySelector("#tickets_no")
console.log("hello");


var count=0;
ticketIncrease.addEventListener("click",()=>{
    if(count>=0){
        ticketDecrease.classList.remove("disabled")
        bookButton.classList.remove("disabled")
    }
    if(count<10){
        count++;
        numberOfTickets.innerHTML=count;
    }if(count==10){
        ticketIncrease.classList.add("disabled")
        alertMessage.classList.remove("d-none")
        
    }
})


ticketDecrease.addEventListener("click",()=>{
    if(count>0){
        count--;
        numberOfTickets.innerHTML=count;
        // bookButton.classList.remove("disabled")       
    }if(count==0){
        ticketDecrease.classList.add("disabled")
        bookButton.classList.add("disabled")
    }if(count==9){
        ticketIncrease.classList.remove("disabled")
        alertMessage.classList.add("d-none")
    }
})

// ticketIncrease.onclick = function(){
//     count++;
//     numberOfTickets.innerHTML="hell";
// }