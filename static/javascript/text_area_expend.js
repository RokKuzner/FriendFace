window.addEventListener("load", (e) => {
    let textareas = document.querySelectorAll("textarea")

    for (let textarea of textareas) {
        textarea.addEventListener("input", handle_textarea_input)
    }
})

function handle_textarea_input() {
    let element = this
    let computed_style = window.getComputedStyle(element)

    let required_height = element.scrollHeight
    let max_height = Number(computed_style.maxHeight.slice(0, -2)) //slice(0, -2) returns only the number (ex. 200) instead of ex. 200px

    if (required_height > max_height) {
        required_height = max_height
        element.style.overflowY = "scroll"
    } else {
        element.style.overflowY = "hidden"
    }
    element.style.height = required_height + "px"
}