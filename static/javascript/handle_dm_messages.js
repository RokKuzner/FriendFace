let send_message_form = document.querySelector(".send-message-form")

function display_messages(messages) {
    let content_wrap_element = document.querySelector(".content-wrap")
    content_wrap_element.innerHTML = ""

    let message_div;
    let date;
    let date_str;
    let current_timestamp;
    let seconds_delta;
    let days_delta;
    let datetime_str;
    let message_time_div;
    let message_content_div;

    for (let message of messages) {

        //create a new div element for the message
        message_div = document.createElement("div")
        message_div.id = message.message_id
        message_div.classList.add("message")

        if (message.sender_id == current_user_id) {
            message_div.classList.add("message-mine")
        } else {
            message_div.classList.add("message-other")
        }

        //create a new div element for message time
        date = new Date(message.timestamp*1000)
        current_timestamp = Date.now()

        seconds_delta = Number(current_timestamp - Math.floor(message.timestamp*1000)) / 1000
        seconds_delta = Math.floor(seconds_delta)
        days_delta = seconds_delta / (60 * 60 * 24)
        days_delta = Math.floor(days_delta)

        time_str = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
        if (days_delta == 0) {
            date_str = "Today"
            datetime_str = `${time_str} - ${date_str}`
        } else if (days_delta <= 7) {
            date_str = date.toDateString().substring(0, 3)
            datetime_str = `${time_str} - ${date_str}`
        } else {
            date_str = `${date.getDate()}. ${Number(date.getMonth()+1)}. ${date.getFullYear()}`
            datetime_str = date_str
        }

        message_time_div = document.createElement("div")
        message_time_div.classList.add("time")
        message_time_div.innerText = datetime_str
        message_div.appendChild(message_time_div)

        //create a new div element for message content
        message_content_div = document.createElement("div")
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

    //Set typing status to false
    set_typing_status("false")

    //Send message
    dm_messages_socket.send(JSON.stringify({
        "message": textarea.value
    }))

    //UI stuff
    textarea.value = ""

    submit_btn.innerHTML = 'Send'
    submit_btn.classList.remove("disabled")
})