from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from decorators import login_required
import database as db
from FriendFace.settings import BASE_DIR
import os
from PIL import Image

# Create your views here.
@login_required
def home(request):
    posts = db.get_posts(request.session["current_user"])
    return render(request, 'index.html', {'logged_in':True, 'current_user':request.session['current_user'], 'current_user_id': db.get_users_id_by_username(request.session['current_user']), 'posts':posts[::-1], 'this_url':str('/')})

@login_required
def user(request, user_page):
    posts = db.get_posts_by_user(user_page)
    return render(request, 'user.html', {'logged_in':True, 'current_user':request.session['current_user'], 'current_user_id': db.get_users_id_by_username(request.session['current_user']),'posts':posts[0][::-1], 'user_page':user_page, 'user_page_id':db.get_users_id_by_username(user_page), 'this_url':str('/user/'+user_page), 'total_likes':posts[1], 'total_posts':posts[2]})

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
    then = str(request.GET.get('then', None))
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        if db.validate_user(username, password):
            request.session["current_user"] = username
            if then != 'None':
                return redirect(str(then))
            return redirect('/')
        else:
            messages.error(request, "Username or password is incorrect")
            if then != 'None':
                return redirect(str('/login?then='+str(then)))
            return redirect('/login')
    return render(request, 'login.html', {'logged_in':False, 'then':then})

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

            try:
                a = request.FILES['avatar']
            except:
                messages.error(request, "You must chose an avatar for yourself")
                return redirect('/register')

            filename = os.path.join(BASE_DIR, "media", "avatars", str(user_id+'.jpg'))

            image = Image.open(request.FILES['avatar'])
            croped_img = image.crop(box=(0, 0, min(image.size), min(image.size)))
            croped_img.convert("RGB").save(filename)

            return redirect('/')

    return render(request, 'register.html', {'logged_in':False})

def logout(request):
    request.session["current_user"] = None
    del request.session['current_user']
    return redirect('/login')