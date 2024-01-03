let forms = document.querySelectorAll("form")

for (let form of forms) {
    form.addEventListener("submit", async function(e){
        e.preventDefault()

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
    })
}