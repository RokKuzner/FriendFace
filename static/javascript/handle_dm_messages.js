let send_message_form = document.querySelector(".send-message-form")

function display_messages(messages) {
    let content_wrap_element = document.querySelector(".content-wrap")
    content_wrap_element.innerHTML = ""

    for (let message of messages) {

        //create a new div element for the message
        let message_div = document.createElement("div")
        message_div.id = message.message_id
        message_div.classList.add("message")

        if (message.sender_id == current_user_id) {
            message_div.classList.add("message-mine")
        } else {
            message_div.classList.add("message-other")
        }

        //create a new div element for message time
        let message_time_div = document.createElement("div")
        message_time_div.classList.add("time")
        message_time_div.innerText = message.time_pretty
        message_div.appendChild(message_time_div)

        //create a new div element for message content
        let message_content_div = document.createElement("div")
        message_content_div.classList.add("content")
        message_content_div.innerText = message.content
        message_div.appendChild(message_content_div)
        
        content_wrap_element.appendChild(message_div)
    }
    
    //Scroll to bottom
    content_wrap_element = document.querySelector(".content-wrap")
    content_wrap_element.scrollTop = content_wrap_element.scrollHeight
}

const dm_messages_socket_url = "ws://" + window.location.host + "/ws/dm-messages/" + dm_id
const dm_messages_socket = new WebSocket(dm_messages_socket_url)

dm_messages_socket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    display_messages(data["messages"])
}

send_message_form.addEventListener("submit", async function(e){
    e.preventDefault()

    let textarea = send_message_form.querySelector(".send-message-textarea")
    let submit_btn = send_message_form.querySelector(".send-button");
    submit_btn.classList.add("disabled")
    submit_btn.innerHTML = '<img style="width: 30px;" src="/files/static/icons?file=loading.gif">'

    //Send message
    dm_messages_socket.send(JSON.stringify({
        "message": textarea.value
    }))

    //UI stuff
    textarea.value = ""

    submit_btn.innerHTML = 'Send'
    submit_btn.classList.remove("disabled")
})