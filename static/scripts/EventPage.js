var ticketIncrease = document.querySelector("#increment")
var ticketDecrease = document.querySelector("#decrement")
var bookButton = document.querySelector("#book-button")
var alertMessage=document.querySelector("#alert-msg")

var numberOfTickets = document.querySelector("#tickets_no")
var remainingTickets=document.querySelector("#ticket-remaining")




var count=0;
ticketIncrease.addEventListener("click",()=>{
    // var no_tickets=numberOfTickets.innerHTML
    // no_tickets=parseInt(no_tickets)
    // var ticket_rem=remainingTickets.innerHTML
    // ticket_rem=parseInt(ticket_rem)
    // console.log(no_tickets)
    // if(ticket_rem<no_tickets){
    //     ticketIncrease.classList.add("disabled")
    // }else{
    //     ticketIncrease.classList.contains("disabled")
    //     ticketIncrease.classList.remove("disabled")
    // }
    
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
function getnooftickets(){
    document.getElementById("ticketcount").value=document.getElementById("tickets_no").innerHTML
    return true
}




// ticketIncrease.onclick = function(){
//     count++;
//     numberOfTickets.innerHTML="hell";
// }