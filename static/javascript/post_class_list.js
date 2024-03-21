class Post {
    constructor(element) {
        this.element = element
        this.id = this.element.id
        this.isread = false
        this.in_viewport_for = 0
    }
}

let posts_elements = document.querySelectorAll(".post")

let posts = []
for (let post_element of posts_elements) {
    posts.push(new Post(post_element))
}