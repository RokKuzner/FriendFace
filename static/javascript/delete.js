let del = document.querySelector(".delete")
let over = document.querySelector(".over")

let del_btn = document.getElementById("delete-delete")
let cancel_btn = document.getElementById("delete-cancel")

let currently_deleting = null

for (let post of posts) {
    let a = post.element.querySelector(".posttop .posttopdelete")
    if (a) {
        a.addEventListener("click", (e) => {
            del.classList.remove("hidden")
            over.classList.remove("hidden")

            currently_deleting = post.id
        })
    }
}

del_btn.addEventListener("click", async function(e) {
    if (currently_deleting != null) {
        del_btn.classList.add("disabled")
        del_btn.innerHTML = '<img style="width: 22px;" src="/files/static/icons?file=loading.gif">'

        let url = String(window.location.origin)+"/api/deletepost?id=" + String(currently_deleting)

        let response = await fetch(url);
        let json_response = await response.json();

        if (json_response["status"] == "succes") {
            document.getElementById(currently_deleting).parentElement.removeChild(document.getElementById(currently_deleting))

            currently_deleting = null

            del_btn.classList.remove("disabled")
            del_btn.innerHTML = "Delete"
            del.classList.add("hidden")
            over.classList.add("hidden")
        } else {
            currently_deleting = null

            del_btn.classList.remove("disabled")
            del_btn.innerHTML = "Delete"
            del.classList.add("hidden")
            over.classList.add("hidden")
        }
    }
})

cancel_btn.addEventListener("click", (e) => {
    currently_deleting = null
    del.classList.add("hidden")
    over.classList.add("hidden")
})