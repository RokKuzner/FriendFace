window.addEventListener("load", (e) => {
    let textareas = document.querySelectorAll("textarea")

    for (let textarea of textareas) {
        textarea.addEventListener("input", handle_textarea_input)
    }
})

function handle_textarea_input() {
    let element = this

    let required_height = element.scrollHeight
    if (required_height > 200) {
        required_height = 200
        element.style.overflowY = "scroll"
    }

    element.style.height = required_height.toString() + "px"
}