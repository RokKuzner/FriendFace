async function copy_to_clipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return "succes"
    } catch (err) {
        return err
    }
}

for (let post of document.querySelectorAll(".post")) {
    let share_div = post.querySelector(".commentoptions .sharediv")
    share_div.addEventListener("click", e => {
        let url = String(window.location.href)+"getpost/"+post.id
        copy_to_clipboard(url)
    })
}