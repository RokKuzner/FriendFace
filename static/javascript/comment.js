let forms = document.querySelectorAll(".comment-form")

for (let form of forms) {
    form.addEventListener("submit", async function(e){
        e.preventDefault()

        let submit_btn = form.querySelector(".commentbtndiv");
        submit_btn.classList.add("disabled")
        submit_btn.innerHTML = '<img style="width: 30px;" src="/files/static/icons?file=loading.gif">'

        //Make the request
        let data = new FormData(form)
        let payload = new URLSearchParams(data)

        let url = String(window.location.origin)+"/api/comment"

        let response = await fetch(url, {
            method: "POST",
            body: payload
        })
        let json_response = await response.json()

        //UI stuff
        let comment_input = form.querySelector(".mycommentdiv #posttext")
        if (json_response.status == "succes") {
            comment_input.value = ""
        }

        submit_btn.innerHTML = 'Comment'
        submit_btn.classList.remove("disabled")

        form.parentElement.querySelector(".commentoptions .commentoptioncomments a").innerText = "Comments (" + String(json_response.comments) + ")"
    })
}