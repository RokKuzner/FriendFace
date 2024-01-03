from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.http import JsonResponse
from decorators import login_required
import database as db
from FriendFace.settings import BASE_DIR
import os
from PIL import Image
import algorythms as alg

# Views
@login_required
def readpost(request):
    #Get post id query parameter
    post_id = request.GET.get('post', None)

    if post_id != None:
        db.read_post(request.session["current_user"], post_id)
        return JsonResponse({"status": "succes"}, status=200)

    return JsonResponse({"status": "error", "descriprion":"post_id not provided"}, status=500)

@login_required
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

    count = int(db.get_post_by_post_id(request.session["current_user"], post_id)[2])

    return JsonResponse({"status": "succes", "state":state, "count":count}, status=200)

@login_required
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