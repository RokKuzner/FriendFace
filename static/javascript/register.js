//Vasriables
const inputs = document.querySelectorAll("form input")

const username = inputs[1]
const password_1 = inputs[2]
const password_2 = inputs[3]
const image_input = inputs[4]
const submit_button = document.querySelector("form button")

let last_username_value = username.value+"1"
let last_usename_avalible_respone = null
let previous_usernames = []

const alert_div = document.getElementById("dynamicalert")
alert_div.style.display = "none"

const border_error = "2px rgb(35, 111, 221) solid"
const allowed_image_type = ["image/jpg", "image/jpeg", "image/png"]

//Functions
async function check_inputs() {
    let to_disable = false
    let username_avalible_return = await check_username_taken()

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
    } else if (username.value.includes("..") && to_disable == false) {
        to_disable = true
        username.style.border = border_error

        alert_div.innerText = "Username cannot contain '..'"
    } else if (username.value.includes("/") && to_disable == false) {
        to_disable = true
        username.style.border = border_error

        alert_div.innerText = "Username cannot contain '/'"
    } else if (username.value.includes("\\") && to_disable == false) {
        to_disable = true
        username.style.border = border_error

        alert_div.innerText = "Username cannot contain '\\'"
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

    if (check_image() && to_disable == false) {
        to_disable = true
        image_input.style.border = border_error

        alert_div.innerText = "You must select your profile image"
    } else if (!check_image() && (!allowed_image_type.includes(image_input.files[0].type)) && to_disable == false) {
        to_disable = true
        image_input.style.border = border_error

        alert_div.innerText = "You must select a valid image type"
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
    if (image_input.files.length != 1) {return true}
    return false
}

async function check_username_taken() {
    if (previous_usernames[username.value] != null) {
        return previous_usernames[username.value]
    }

    if (last_username_value == username.value) {
        previous_usernames[username.value] = last_usename_avalible_respone
        return last_usename_avalible_respone
    }
    last_username_value = username.value

    let request_url = window.location.origin + "/api/userexists?user=" + username.value;
    let response = await fetch(request_url);
    let json_response = await response.json();
    last_usename_avalible_respone = json_response["user_exists"]
    previous_usernames[username.value] = json_response["user_exists"]
    return json_response["user_exists"];
}

//When page loads disable submit button
submit_button.classList.add("disabled")

//Check for every input change
username.addEventListener("input", (event) => check_inputs());
password_1.addEventListener("input", (event) => check_inputs());
password_2.addEventListener("input", (event) => check_inputs());
image_input.addEventListener("input", (event) => check_inputs());