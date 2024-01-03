let like_forms = document.querySelectorAll(".likedstuff")

for (let like_form of like_forms) {
    like_form.addEventListener("click", async function (e) {
        let like_img = like_form.querySelector(".likeimg")
        let like_count_div = like_form.querySelector(".likediv")

        let like_form_id = like_form.querySelector("input").value
        let url = String(window.location.origin)+"/apilike?post=" + String(like_form_id)

        let response = await fetch(url);
        let json_response = await response.json();

        if (json_response["state"] == "liked") {
            like_img.src = "/files/static/icons?file=liked.png"
        } else {
            like_img.src = "/files/static/icons?file=like.png"
        }
        like_count_div.innerText = json_response["count"]
    })
}