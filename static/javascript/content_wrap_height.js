let content_wrap_element = document.querySelector(".content-wrap")

let element_classes_to_subtract = ["navbar", "top-corresponder-info", "send-message-form"]

let elements_to_subtract = []
for (let element_class_to_subtract of element_classes_to_subtract) {
    elements_to_subtract.push(document.querySelector("." + element_class_to_subtract))
}


function resize_content_wrap() {
    let content_wrap_height = window.innerHeight

    for (let element_to_subtract of elements_to_subtract) {
        if (element_to_subtract) {
            content_wrap_height -= element_to_subtract.offsetHeight
        }
    }

    content_wrap_element.style.height = content_wrap_height + "px"
}

window.onload = resize_content_wrap
window.onresize = resize_content_wrap

let resize_observer = new ResizeObserver(entries => {
    resize_content_wrap()
})

elements_to_subtract.forEach(element => {
    if (element) {
        resize_observer.observe(element)
    }
})