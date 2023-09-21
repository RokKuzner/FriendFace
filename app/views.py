from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from decorators import login_required
import database as db

# Create your views here.
@login_required
def home(request):
    posts = db.get_posts()[::-1]
    posts_return = []
    for post in posts:
        if db.user_liked_post(request.session["current_user"], post[4]):
            posts_return.append(post+(True,db.get_comments_by_parrent_post(post[4])[::-1]))
        else:
            posts_return.append(post+(False,db.get_comments_by_parrent_post(post[4])[::-1]))
    return render(request, 'index.html', {'logged_in':True, 'current_user':request.session['current_user'], 'posts':posts_return})

@login_required
def user(request, user_page):
    posts = db.get_posts_by_user(user_page)[::-1]
    posts_return = []
    for post in posts:
        if db.user_liked_post(request.session["current_user"], post[4]):
            posts_return.append(post+(True,db.get_comments_by_parrent_post(post[4])[::-1]))
        else:
            posts_return.append(post+(False,db.get_comments_by_parrent_post(post[4])[::-1]))
    return render(request, 'user.html', {'logged_in':True, 'current_user':request.session['current_user'], 'posts':posts_return, 'user_page':user_page})

@login_required
def like(request):
    post_id = request.GET.get('post', None)
    user = request.GET.get('user', None)
    if user != request.session["current_user"]:
        return redirect('/')
    if db.user_liked_post(user, post_id):
        db.dislike_post(user, post_id)
    else:
        db.like_post(user, post_id)
    return redirect('/')

@login_required
def comment(request):
    if request.method == 'POST':
        content = request.POST['comment_content']
        parrent_id = request.POST['comment_parrent_id']
        print(content, parrent_id)
        db.new_comment(request.session['current_user'], content, parrent_id)
    return redirect('/')

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
            return redirect('login')
    return render(request, 'login.html', {'logged_in':False})

def register(request):
    if request.method == 'POST':
        username = request.POST['user']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if db.user_exists(username):
            messages.error(request, "User with this username allready exists")
            return redirect('register')
        elif len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return redirect('register')
        elif password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        elif "," in username:
            messages.error(request, "Username cannot contain a comma")
            return redirect('register')
        else:
            db.add_user(username, password1)
            request.session["current_user"] = username
            return redirect('/')

    return render(request, 'register.html', {'logged_in':False})

def logout(request):
    request.session["current_user"] = None
    del request.session['current_user']
    return redirect('login')