let error_div = document.querySelector(".new-dm-errors")
let username_input = document.querySelector(".new-dm-input")
let submit_button = document.querySelector(".new-dm-submit-button")

let last_username_value = username_input.value+"1"
let last_usename_avalible_respone = null
let previous_usernames = []

async function check_username_taken() {
    if (previous_usernames[username_input.value] != null) {
        return previous_usernames[username_input.value]
    }

    if (last_username_value == username_input.value) {
        previous_usernames[username_input.value] = last_usename_avalible_respone
        return last_usename_avalible_respone
    }
    last_username_value = username_input.value

    let request_url = window.location.origin + "/api/userexists?user=" + username_input.value;
    let response = await fetch(request_url);
    let json_response = await response.json();
    last_usename_avalible_respone = json_response["user_exists"]
    previous_usernames[username_input.value] = json_response["user_exists"]
    return json_response["user_exists"];
}

async function check_input() {
    let username_taken = await check_username_taken()
    
    if (username_taken == false) {
        error_div.innerText = "User does not exist"
        error_div.classList.remove("hidden")
        submit_button.classList.add("disabled")

        return
    }
    if (username_input.value == current_user_username) {
        error_div.innerText = "You cannot create a DM with yourself"
        error_div.classList.remove("hidden")
        submit_button.classList.add("disabled")

        return
    }

    error_div.innerText = ""
    error_div.classList.add("hidden")
    submit_button.classList.remove("disabled")
}

username_input.addEventListener("input", async (event) => await check_input());