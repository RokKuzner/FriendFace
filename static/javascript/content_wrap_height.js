let content_wrap_element = document.querySelector(".content-wrap")
let nav_element = document.querySelector(".navbar")

let content_wrap_height = window.innerHeight - nav_element.offsetHeight

content_wrap_element.style.height = content_wrap_height + "px"

console.log(content_wrap_element)
console.log(nav_element)
console.log(content_wrap_height)