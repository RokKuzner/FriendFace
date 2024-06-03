var last_messages = []

async function get_messages() {
    let request_url = window.location.origin + "/api/getdmmessages/" + dm_id
    let response = await fetch(request_url)
    let json_response = await response.json()

    return json_response["messages"]
}

async function display_messages() {
    let messages = await get_messages()

    if (last_messages.length == 0 || messages[messages.length - 1].message_id != last_messages[last_messages.length - 1].message_id) {
        last_messages = messages

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
    } else {
        for (let message of messages) {
            let message_element = document.getElementById(message.message_id)

            if (message_element == null) {
                continue
            }

            let message_time_div = message_element.querySelector(".time")
            message_time_div.innerText = message.time_pretty
        }
    }
}

window.addEventListener("load", async () => {
    await display_messages()

    //Scroll to bottom
    let content_wrap_element = document.querySelector(".content-wrap")
    content_wrap_element.scrollTop = content_wrap_element.scrollHeight
})

setInterval(display_messages, 1000)