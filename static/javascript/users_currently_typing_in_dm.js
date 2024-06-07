let send_message_text_area = document.querySelector(".send-message-textarea")
let typing_status_element = document.querySelector(".top-corresponder-info-username .typing-status")

async function get_users_typing() {
    let request_url = window.location.origin + "/api/getcurrentlytyping?dm_id=" + dm_id
    let response = await fetch(request_url)
    let json_response = await response.json()

    return json_response["users typing"]
}

async function set_user_typing_status(typing_status) {
    let request_url = window.location.origin + "/api/settypingstatus?dm_id=" + dm_id + "&typing=" + typing_status
    let response = await fetch(request_url)
}

send_message_text_area.addEventListener("input", () => {
    if (send_message_text_area.value == "") {
        set_user_typing_status("false")
    } else {
        set_user_typing_status("true")
    }
})

async function update_typing_status() {
    let users_typing = await get_users_typing()
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

setInterval(update_typing_status, 500)