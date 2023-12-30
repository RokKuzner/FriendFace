const user_img_item = document.getElementById("user_img_icon")
const user_menu = document.getElementById("user_menu")
const body_element = document.getElementById("myBody")

let last_in = new Date().getTime() - 10000

function chech_hover() {
    if ((user_img_item.matches(":hover")) || user_menu.matches(":hover")) {
        user_menu.classList.remove("hidden");
        last_in = new Date().getTime()
    } else {
        if ((new Date().getTime() - last_in) < (300)) {

        } else {
            user_menu.classList.add("hidden");
        }
    }
}

setInterval(chech_hover, 5)