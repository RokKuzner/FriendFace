const inputs = document.querySelectorAll("form input")

const username = inputs[1]
const password_1 = inputs[2]
const password_2 = inputs[3]
const image_input = inputs[4]
const submit_button = document.querySelector("form button")

const alert_div = document.getElementById("dynamicalert")
alert_div.style.display = "none"

function check_inputs() {
    let to_disable = false

    if (username.value.length == 0 && to_disable == false) {
        to_disable = true
        username.style.border = "2px red solid"

        alert_div.innerText = "You must set a username"
    } else if (username.value.includes(",") && to_disable == false) {
        to_disable = true
        username.style.border = "2px red solid"

        alert_div.innerText = "Username cannot contain a comma"
    } else {
        username.style.border = ""
    }

    if (check_password1() && to_disable == false) {
        to_disable = true
        password_1.style.border = "2px red solid"

        alert_div.innerText = "Password must be at least 6 characters long"
    } else {
            password_1.style.border = ""
    }

    if (check_password2()  && to_disable == false) {
            to_disable = true
            password_2.style.border = "2px red solid"

            alert_div.innerText = "Passwords don't match"
    } else {
            password_2.style.border = ""
    }

    if (check_image()  && to_disable == false) {
        to_disable = true
        image_input.style.border = "2px red solid"

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

setInterval(check_inputs, 300)
