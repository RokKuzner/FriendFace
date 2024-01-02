class Post {
    constructor(element) {
        this.element = element
        this.id = this.element.id
        this.isread = false
        this.in_viewport_for = 0
    }
}

function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}


let posts_elements = document.querySelectorAll(".post")
const http = new XMLHttpRequest()

let posts = []
for (let post_element of posts_elements) {
    posts.push(new Post(post_element))
}

setInterval(async () => {
    for (let post of posts) {
        if (isInViewport(post.element) && (post.isread == false)) {
            if (post.in_viewport_for >= 2) {
                await fetch(String(window.location.href)+"readpost?post="+post.id)

                post.isread = true
            } else {
                post.in_viewport_for += 0.5
            }
        } else {
            post.in_viewport_for = 0
        }
    }
}, 500)