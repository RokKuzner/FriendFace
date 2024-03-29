let content_wrap_element = document.querySelector(".content-wrap")
let nav_element = document.querySelector(".navbar")

function resize_content_wrap() {
    let content_wrap_height;
    if (nav_element) {
        content_wrap_height = window.innerHeight - nav_element.offsetHeight
    } else {
        content_wrap_height = window.innerHeight
    }

    content_wrap_element.style.height = content_wrap_height + "px"
}

window.onload = resize_content_wrap
window.onresize = resize_content_wrap