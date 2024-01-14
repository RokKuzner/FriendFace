let post_btn = document.getElementById("postbtn")
let post_text = document.getElementById("posttext")
let post_form = document.getElementById("post-form")

post_form.addEventListener("submit", async function(e){
    e.preventDefault()

    let url = window.location.origin + "/api/post"

    if (post_btn.classList.contains("disabled")) {
        return null
    }
    
    if ( (!(post_text.value == '')) && (!(post_text.value == (' '*post_text.value.length))) ) {
        post_btn.classList.add("disabled")
        post_btn.innerHTML = '<img style="width: 30px;" src="/files/static/icons?file=loading.gif">'

        let data = new FormData(post_form)
        let payload = new URLSearchParams(data)

        let response = await fetch(url, {
            method: "POST",
            body: payload
        })
        let json_res = await response.json()

        if (json_res["status"] == "succes") {
            window.location.reload()
        }

        post_btn.innerHTML = 'Post'
        post_btn.classList.remove("disabled")
    }
})