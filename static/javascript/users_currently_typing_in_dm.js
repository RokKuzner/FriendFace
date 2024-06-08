let send_message_text_area = document.querySelector(".send-message-textarea")
let typing_status_element = document.querySelector(".top-corresponder-info-username .typing-status")

let last_typing_data = {"time":0, "is_typing":"false"}

function update_typing_status(users_typing) {
    let corresponder_is_typing = false

    for (let user_typing of users_typing) {
        if (user_typing.user_id == coresponed_id) {
            corresponder_is_typing = true
            break
        }
    }

    if (corresponder_is_typing) {
        typing_status_element.classList.remove("hidden")
    } else {
        typing_status_element.classList.add("hidden")
    }
}

const dm_typing_socket_url = "ws://" + window.location.host + "/ws/dm-typing/" + dm_id
const dm_typing_socket = new WebSocket(dm_typing_socket_url)

function set_typing_status(status) {
    if (status != "true" && status != "false") {
        return "status can be a string true or false"
    }

    //save the data
    last_typing_data["time"] = Date.now()
    last_typing_data["is_typing"] = status

    //send typing status to server
    dm_typing_socket.send(JSON.stringify({
        "is_typing": status
    }))
}

dm_typing_socket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    update_typing_status(data["users typing"])
}

send_message_text_area.addEventListener("input", () => {
    let is_typing;

    if (send_message_text_area.value == "") {
        is_typing = "false"
    } else {
        is_typing = "true"
    }

    set_typing_status(is_typing)
})

setInterval(()=>{
    if ( Date.now() - last_typing_data["time"] > 3000 && last_typing_data["is_typing"] == "true") {
        set_typing_status("false")
    }
}, 500)