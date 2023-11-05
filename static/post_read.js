function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

let posts = document.querySelectorAll(".post")
let read_posts_this_session = []
const http = new XMLHttpRequest()

function handle() {
    let indx = 0
    while (indx < posts.length) {
        if (isInViewport(posts[indx]) && (read_posts_this_session.includes(posts[indx]) == false)) {
            let url = String(window.location.href)+"readpost?post="+posts[indx].id
            http.open("GET", String(url))
            http.send()
            read_posts_this_session.push(posts[indx])
        }
        indx ++
    }
}

setInterval(handle, 500)