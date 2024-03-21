function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

async function handle() {
    for (let post of posts) {
        if (isInViewport(post.element) && (post.isread == false)) {
            if (post.in_viewport_for >= 2) {
                await fetch(String(window.location.origin)+"/api/readpost?post="+post.id)

                post.isread = true
            } else {
                post.in_viewport_for += 0.5
            }
        } else {
            post.in_viewport_for = 0
        }
    }
}

setInterval(async () => {
    await handle()
}, 500)