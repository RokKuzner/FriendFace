let send_form = document.querySelector(".send-message-form")

send_form.addEventListener("submit", async function(e){
    e.preventDefault()

    let submit_btn = send_form.querySelector(".send-button");
    submit_btn.classList.add("disabled")
    submit_btn.innerHTML = '<img style="width: 30px;" src="/files/static/icons?file=loading.gif">'

    //Make the request
    let data = new FormData(send_form)
    let payload = new URLSearchParams(data)

    let url = String(window.location.origin)+"/api/newdmmessage"

    let response = await fetch(url, {
        method: "POST",
        body: payload
    })
    let json_response = await response.json()

    //UI stuff
    let textarea = send_form.querySelector(".send-message-textarea")
    if (json_response.status == "succes") {
        textarea.value = ""
    }

    submit_btn.innerHTML = 'Send'
    submit_btn.classList.remove("disabled")
})