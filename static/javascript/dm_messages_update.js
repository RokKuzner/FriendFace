async function get_messages() {
    let request_url = window.location.origin + "/api/getdmmessages/" + dm_id
    let response = await fetch(request_url)
    let json_response = await response.json()

    return json_response["messages"]
}

async function display_messages() {
    let messages = await get_messages()
    let content_wrap_element = document.querySelector(".content-wrap")

    content_wrap_element.innerHTML = ""
    for (let message of messages) {

        //create a new div element for the message
        let message_div = document.createElement("div")
        message_div.classList.add("message")

        if (message.sender_id == current_user_id) {
            message_div.classList.add("message-mine")
        } else {
            message_div.classList.add("message-other")
        }

        //create a new div element for message content
        let message_content_div = document.createElement("div")
        message_content_div.classList.add("content")
        message_content_div.innerText = message.content

        //appent the message content div to the message div
        message_div.appendChild(message_content_div)


        content_wrap_element.appendChild(message_div)
    }
}

window.addEventListener("load", async () => {
    await display_messages()

    //Scroll to bottom
    let content_wrap_element = document.querySelector(".content-wrap")
    content_wrap_element.scrollTop = content_wrap_element.scrollHeight
})

setInterval(display_messages, 500)