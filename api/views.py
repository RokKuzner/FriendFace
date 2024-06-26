from django.http import JsonResponse
from decorators import login_required_json_response
import database as db
import FriendChatTyping as fct

# Views
@login_required_json_response
def readpost(request):
    #Get post id query parameter
    post_id = request.GET.get('post', None)

    if post_id != None:
        db.read_post(request.session["current_user"], post_id)
        return JsonResponse({"status": "succes"}, status=200)

    return JsonResponse({"status": "error", "descriprion":"post_id not provided"}, status=500)

@login_required_json_response
def like(request):
    #Get query parameter
    post_id = request.GET.get('post', None)

    user = request.session["current_user"]

    #If post is allready liked
    if db.user_liked_post(user, post_id):
        #Dislike post
        db.dislike_post(user, post_id)

        state = "disliked"
    #If post isn't allready liked
    else:
        #Like post
        db.like_post(user, post_id)

        state = "liked"

        #Add genre to user's interests
        genre = db.get_post_genre(post_id)
        db.add_user_interest(user, genre)

    count = int(db.get_post_by_post_id(request.session["current_user"], post_id)["likes"])

    return JsonResponse({"status": "succes", "state":state, "count":count}, status=200)

@login_required_json_response
def comment(request):
    if request.method == 'POST':
        content = request.POST['comment_content']
        parrent_id = request.POST['comment_parrent_id']
        db.new_comment(request.session['current_user'], content, parrent_id)

        number_of_comments = len(db.get_comments_by_parrent_post(parrent_id))
        return JsonResponse({"status": "succes", "comments":int(number_of_comments)}, status=200)

    return JsonResponse({"status": "error", "descriprion":"only post method allowed"}, status=500)

def userexists(request):
    user = request.GET.get('user', None)
    if user == None:
        return JsonResponse({"status": "error", "description":"user not provided"}, status=500)
    return JsonResponse({"status": "succes", "user":user, "user_exists":db.user_exists(user)})

@login_required_json_response
def post(request):
    content = request.POST['post_content']

    db.new_post(request.session['current_user'], content)

    return JsonResponse({"status": "succes"}, status=200)

@login_required_json_response
def delete_post(request):
    id = request.GET.get('id', None)

    if id == None:
        return JsonResponse({"status": "error", "descriprion":"no post id provided"}, status=500)

    post = db.get_post_by_post_id(request.session['current_user'], id)
    if not post:
        return JsonResponse({"status": "error", "descriprion":"no post with that id"}, status=500)
    
    post_user = post["author_username"]
    if post_user != request.session['current_user']:
        return JsonResponse({"status": "error", "descriprion":"cannot delete posts that aren't yours"}, status=500)
    
    db.delete_post(id)

    return JsonResponse({"status": "succes", "post_id":id}, status=200)

@login_required_json_response
def set_currently_typing_in_dm(request):
    current_user_id = db.get_users_id_by_username(request.session["current_user"])

    dm_id = str(request.GET.get('dm_id', None))
    is_typing = str(request.GET.get('typing', None))

    if dm_id == "None":
        return JsonResponse({"status": "error", "descriprion":"dm id not provided"}, status=500)
    if not db.dm_exists_by_id(dm_id):
        return JsonResponse({"status": "error", "descriprion":"provided dm id does not exist"}, status=500)
    
    if is_typing == "None":
        return JsonResponse({"status": "error", "descriprion":"typing status not provided"}, status=500)
    if is_typing != "true" and is_typing != "false":
        return JsonResponse({"status": "error", "descriprion":"provided typing status is not valid (true or false only allowed)"}, status=500)
    
    if is_typing == "true":
        fct.start_typing(dm_id, current_user_id)
    else:
        fct.stop_typing(dm_id, current_user_id)

    return JsonResponse({"status": "succes"}, status=200)

@login_required_json_response
def get_currently_typing_in_dm(request):
    current_user_id = db.get_users_id_by_username(request.session["current_user"])

    dm_id = str(request.GET.get('dm_id', None))

    if dm_id == "None":
        return JsonResponse({"status": "error", "descriprion":"dm id not provided"}, status=500)
    if not db.dm_exists_by_id(dm_id):
        return JsonResponse({"status": "error", "descriprion":"provided dm id does not exist"}, status=500)
    
    if current_user_id not in db.get_dm_members(dm_id):
        return JsonResponse({"status": "error", "descriprion":"user not in dm"}, status=500)
    
    return JsonResponse({"status": "succes", "users typing": fct.get_currently_typing_in_dm(dm_id)}, status=200)