const inputs = document.querySelectorAll("form input")

const username = inputs[1]
const password_1 = inputs[2]
const password_2 = inputs[3]
const image_input = inputs[4]
const submit_button = document.querySelector("form button")

let last_username_value = username.value+"1"
let last_usename_avalible_respone = null

const alert_div = document.getElementById("dynamicalert")
alert_div.style.display = "none"

const border_error = "2px red solid"

async function check_inputs() {
    let to_disable = false
    let username_avalible_return = await check_username_avalible()

    if (username_avalible_return && to_disable == false) {
        to_disable = true
        username.style.border = border_error

        alert_div.innerText = "Username allready taken"
    } else if (username.value.length == 0 && to_disable == false) {
        to_disable = true
        username.style.border = border_error

        alert_div.innerText = "You must set a username"
    } else if (username.value.includes(",") && to_disable == false) {
        to_disable = true
        username.style.border = border_error

        alert_div.innerText = "Username cannot contain a comma"
    } else {
        username.style.border = ""
    }

    if (check_password1() && to_disable == false) {
        to_disable = true
        password_1.style.border = border_error

        alert_div.innerText = "Password must be at least 6 characters long"
    } else {
            password_1.style.border = ""
    }

    if (check_password2()  && to_disable == false) {
            to_disable = true
            password_2.style.border = border_error

            alert_div.innerText = "Passwords don't match"
    } else {
            password_2.style.border = ""
    }

    if (check_image()  && to_disable == false) {
        to_disable = true
        image_input.style.border = border_error

        alert_div.innerText = "You must select your profile image"
    } else {
        image_input.style.border = ""
    }

    if (to_disable == true) {
        if (!(submit_button.classList.contains("disabled"))) {
            submit_button.classList.add("disabled")
        }
        alert_div.style.display = ""
    } else {
        if (submit_button.classList.contains("disabled")) {
            submit_button.classList.remove("disabled")
        }
        alert_div.style.display = "none"
    }
}

function check_password1() {
    if (password_1.value.length < 6) {return true}
    return false
}

function check_password2() {
    if (password_1.value != password_2.value) {return true}
    return false
}

function check_image() {
    if (image_input.files.length == 0) {return true}
    return false
}

async function check_username_avalible() {
    if (last_username_value == username.value) {
        return last_usename_avalible_respone
    }
    last_username_value = username.value

    let request_url = window.location.origin + "/userexists?user=" + username.value;
    let response = await fetch(request_url);
    let json_response = await response.json();
    last_usename_avalible_respone = json_response["user_exists"]
    return json_response["user_exists"];
}

setInterval(check_inputs, 300)
