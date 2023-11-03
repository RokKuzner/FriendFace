console.log(current_user)
let post_btn = document.getElementById("postbtn")
let post_text = document.getElementById("posttext")
let like_btn = document.getElementById("like")

function post_click() {
    let parts_of_url = String(window.location.href).split("/")
    let redirect_url = parts_of_url[0] + "post?user="+current_user+"&content="+post_text.value
    
    if ( (!(post_text.value == '')) && (!(post_text.value == (' '*post_text.value.length))) ) {
        window.location.replace(redirect_url);
    }
}

function like_click() {
    console.log('like!!')
}

post_btn.addEventListener("click", post_click)
like_btn.addEventListener("click", like_click)