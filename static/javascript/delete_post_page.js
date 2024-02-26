let del = document.querySelector(".delete")
let over = document.querySelector(".over")

let del_btn = document.getElementById("delete-delete")
let cancel_btn = document.getElementById("delete-cancel")

let post_element = document.querySelector(".post")

let post_top_del_btn = post_element.querySelector(".posttop .postpagetopdelete")
if (post_top_del_btn) {
    post_top_del_btn.addEventListener("click", (e) => {
        del.classList.remove("hidden")
        over.classList.remove("hidden")

        document.body.style = "overflow-y: hidden;"
    })
}

del_btn.addEventListener("click", async function(e) {
    del_btn.classList.add("disabled")
    del_btn.innerHTML = '<img style="width: 22px;" src="/files/static/icons?file=loading.gif">'

    let url = String(window.location.origin)+"/api/deletepost?id=" + String(post_id)

    let response = await fetch(url);
    let json_response = await response.json();

    if (json_response["status"] == "succes") {
        window.location.href = String(window.location.origin) + "/user/" + user
    }

    del_btn.classList.remove("disabled")
    del_btn.innerHTML = "Delete"
    del.classList.add("hidden")
    over.classList.add("hidden")

    document.body.style = "overflow-y: scroll;"
})

cancel_btn.addEventListener("click", (e) => {
    del.classList.add("hidden")
    over.classList.add("hidden")

    document.body.style = "overflow-y: scroll;"
})