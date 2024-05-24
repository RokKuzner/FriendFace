let content_wrap_element = document.querySelector(".content-wrap")

let element_classes_to_subtract = ["navbar", "top-corresponder-info"]

function resize_content_wrap() {
    let content_wrap_height = window.innerHeight

    for (let element_class_to_subtract of element_classes_to_subtract) {
        let element_to_subtract = document.querySelector("." + element_class_to_subtract)

        if (element_to_subtract) {
            content_wrap_height -= element_to_subtract.offsetHeight
        }
    }

    content_wrap_element.style.height = content_wrap_height + "px"
}

window.onload = resize_content_wrap
window.onresize = resize_content_wrap