from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from decorators import login_required
import database as db
from FriendFace.settings import BASE_DIR
import os

# Create your views here.
@login_required
def home(request):
    posts = db.get_posts()[::-1]
    posts_return = []
    for post in posts:
        if db.user_liked_post(request.session["current_user"], post[4]):
            posts_return.append(post+(True,db.get_comments_by_parrent_post(post[4])[::-1], db.get_users_id_by_username(post[0])))
        else:
            posts_return.append(post+(False,db.get_comments_by_parrent_post(post[4])[::-1], db.get_users_id_by_username(post[0])))
    return render(request, 'index.html', {'logged_in':True, 'current_user':request.session['current_user'], 'current_user_id': db.get_users_id_by_username(request.session['current_user']), 'posts':posts_return, 'this_url':str('/')})

@login_required
def user(request, user_page):
    posts = db.get_posts_by_user(user_page)[::-1]
    posts_return = []

    total_likes = 0
    total_posts = 0

    for post in posts:
        total_posts += 1
        total_likes += int(post[2])
        if db.user_liked_post(request.session["current_user"], post[4]):
            posts_return.append(post+(True,db.get_comments_by_parrent_post(post[4])[::-1], db.get_users_id_by_username(post[0])))
        else:
            posts_return.append(post+(False,db.get_comments_by_parrent_post(post[4])[::-1], db.get_users_id_by_username(post[0])))

    return render(request, 'user.html', {'logged_in':True, 'current_user':request.session['current_user'], 'current_user_id': db.get_users_id_by_username(request.session['current_user']),'posts':posts_return, 'user_page':user_page, 'user_page_id':db.get_users_id_by_username(user_page), 'this_url':str('/user/'+user_page), 'total_likes':total_likes, 'total_posts':total_posts})

@login_required
def like(request):
    post_id = request.GET.get('post', None)
    user = request.GET.get('user', None)
    redirect_to = request.GET.get('redirect_to', None)
    if user != request.session["current_user"]:
        return redirect('/login')
    if db.user_liked_post(user, post_id):
        db.dislike_post(user, post_id)
    else:
        db.like_post(user, post_id)
    return redirect('/') if redirect_to == None else redirect(redirect_to)

@login_required
def comment(request):
    if request.method == 'POST':
        content = request.POST['comment_content']
        parrent_id = request.POST['comment_parrent_id']
        redirect_to = request.POST['redirect_to']
        db.new_comment(request.session['current_user'], content, parrent_id)
    return redirect(redirect_to)

@login_required
def post(request):
    user_posting = request.GET.get('user', None)
    content = request.GET.get('content', None)
    if user_posting == request.session['current_user']:
        db.new_post(user_posting, content)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        if db.validate_user(username, password):
            request.session["current_user"] = username
            return redirect('/')
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect('/login')
    return render(request, 'login.html', {'logged_in':False})

def register(request):
    if request.method == 'POST':
        username = request.POST['user']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if db.user_exists(username):
            messages.error(request, "User with this username allready exists")
            return redirect('/register')
        elif len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return redirect('/register')
        elif password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('/register')
        elif "," in username:
            messages.error(request, "Username cannot contain a comma")
            return redirect('/register')
        else:
            user_id = db.add_user(username, password1)
            request.session["current_user"] = username

            filename = os.path.join(BASE_DIR, "media", "avatars", str(user_id+'.jpg'))
            with open(filename, "wb") as f:
                f.write(request.FILES['avatar'].read())

            return redirect('/')

    return render(request, 'register.html', {'logged_in':False})

def logout(request):
    request.session["current_user"] = None
    del request.session['current_user']
    return redirect('/login')