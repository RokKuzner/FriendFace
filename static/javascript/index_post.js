let post_btn = document.getElementById("postbtn")
let post_text = document.getElementById("posttext")

async function post_click() {
    let url = window.location.origin + "/api/post"

    if (post_btn.classList.contains("disabled")) {
        return null
    }
    
    if ( (!(post_text.value == '')) && (!(post_text.value == (' '*post_text.value.length))) ) {
        post_btn.classList.add("disabled")
        post_btn.innerHTML = '<img style="width: 30px;" src="/files/static/icons?file=loading.gif">'

        let data = new URLSearchParams();
        data.append("post_content", post_text.value)

        let response = await fetch(url, {
            method: "POST",
            body: data
        })
        let json_res = await response.json()

        if (json_res["status"] == "succes") {
            window.location.reload()
        }

        post_btn.innerHTML = 'Post'
        post_btn.classList.remove("disabled")
    }
}

post_btn.addEventListener("click", async () => {
    await post_click()
})