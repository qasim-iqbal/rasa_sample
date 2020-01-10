const inputMessage = document.getElementById("txtMessage")
const submitButton = document.getElementById("btnSubmit")

submitButton.addEventListener("click",addResponse,false);

// make http request object
function Get(yourUrl, requestData){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);

    Httpreq.send(requestData);
    return Httpreq.responseText;          
}


function createMessageBox(message, isBot, time){

    console.log(message, isBot, time)

    var messageBox = document.createElement('div')


    var imgAvatar = document.createElement('img')
    imgAvatar.style = "width:100%;"
    imgAvatar.alt = "Avatar"
   

    var pMessage = document.createElement('p')
    pMessage.textContent = message

    var spanTime = document.createElement('span')
    spanTime.textContent = time

    // set elements attribute
    if (isBot == false){
        messageBox.className = "container darker"
        spanTime.className = "time-left"
        imgAvatar.className = "right"
        imgAvatar.src = "./img/chatbot.png"

    } else {
        messageBox.className = "container"
        spanTime.className = "time-right"
        imgAvatar.className = "left"
        imgAvatar.src = "./img/user.jpg"
    }

    messageBox.appendChild(imgAvatar)
    messageBox.appendChild(pMessage)
    messageBox.appendChild(spanTime)

    document.body.appendChild(messageBox)
}

function addResponse(){

    var now = new Date();
    var time = now.getHours() +":"+now.getMinutes()+":"+now.getSeconds()

    // take user message
    createMessageBox(inputMessage.value,true, time.toString())

    // make a get request for the response from chatbot api
    url = "http://127.0.0.1:5004/chat"

    // var json_obj = JSON.parse(Get(url))
    var items = {
        'sender': 'default',
        'message': inputMessage.value,
    };
    let dataToRecieved=""; 
    

    console.log(items)


    $.ajax({
        type: "POST",
        url: url,
        data: items,
        dataType: 'json'
    }).done(function(data){
        console.log(data)
        // alert(data['response']);
        if(new RegExp('([a-zA-Z0-9]+://)?([a-zA-Z0-9_]+:[a-zA-Z0-9_]+@)?([a-zA-Z0-9.-]+\\.[A-Za-z]{2,4})(:[0-9]+)?(/.*)?').test(data['response'])) 
        {
            alert("url inside");
        }
        createMessageBox(data['response'],false, time.toString())

        // clear text
        inputMessage.value = ""
    })




}
