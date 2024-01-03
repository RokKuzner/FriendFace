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

allowed_image_type = ["image/jpg", "image/jpeg", "image/png"]

# Create your views here.
@login_required
def home(request):
    #Get personalized posts for cuu+rrrent user
    posts = alg.get_personalized_posts(request.session['current_user'])

    return render(request, 'index.html', {'logged_in':True, 'current_user':request.session['current_user'],
                                          'current_user_id': db.get_users_id_by_username(request.session['current_user']),
                                          'posts':posts[::-1], 'this_url':str('/')})

@login_required
def user(request, user_page):
    #Get all posts posted my user
    posts = db.get_posts_by_user(user_page, request.session['current_user'])

    #Check if user's page is current user's page
    if request.session['current_user'] == user_page:
        is_my_page = True
    else:
        is_my_page = False

    return render(request, 'user.html', {'logged_in':True, 'current_user':request.session['current_user'],
                                         'current_user_id': db.get_users_id_by_username(request.session['current_user']),
                                         'posts':posts[0][::-1], 'user_page':user_page, 'user_page_id':db.get_users_id_by_username(user_page),
                                         'followers':db.get_folowers_n(user_page),
                                         'this_url':str('/user/'+user_page), 'total_likes':posts[1], 'total_posts':posts[2],
                                         'is_following':db.is_following_user(request.session['current_user'], user_page),
                                         'is_my_page':is_my_page})

@login_required
def follow(request, user):
    #Get "redirect to" query parameter
    redirect_to = request.GET.get('redirect_to', None)

    #Follow user
    db.follow_user(request.session["current_user"], user)

    #Redirect
    return redirect('/') if redirect_to == None else redirect(redirect_to)

@login_required
def unfollow(request, user):
    #Get "redirect to" query parameter
    redirect_to = request.GET.get('redirect_to', None)

    #Unfollow user
    db.unfollow_user(request.session["current_user"], user)

    #Redirect
    return redirect('/') if redirect_to == None else redirect(redirect_to)

@login_required
def editprofile(request, user):
    #Redirect to logout if the edit page is not current user's
    if user != request.session['current_user']:
        return redirect("/logout")
    
    #Construct the redirect url
    redirect_url = "/user/"+user+"/edit"

    #If changing password
    if request.method == 'POST' and request.POST["change"] == "password":
        #Get the input values
        old_password = request.POST["oldpassword"]
        new_password = request.POST["newpassword"]

        if old_password == new_password:
            messages.error(request, "The provided passwords are the same")
            return redirect(redirect_url)
        if not db.validate_user(user, old_password):
            messages.error(request, "Incorect old(current) password")
            return redirect(redirect_url)
        if len(new_password) < 6:
            messages.error(request, "New password must be at least 6 characters long")
            return redirect(redirect_url)
        
        db.change_password(user, new_password)
        messages.success(request, "Succesfully changed password")
        return redirect(redirect_url)
    
    if request.method == 'POST' and request.POST["change"] == "image":
        if ("avatar" not in request.FILES) or (request.FILES['avatar'].content_type not in allowed_image_type):
            messages.success(request, "Invalid image type")
            return redirect(redirect_url)

        filename = os.path.join(BASE_DIR, "media", "avatars", str(db.get_users_id_by_username(user)+'.jpg'))

        if os.path.exists(filename):
            os.remove(filename)

        image = Image.open(request.FILES['avatar'])
        croped_img = image.crop(box=(0, 0, min(image.size), min(image.size)))
        croped_img.convert("RGB").save(filename)

        messages.success(request, "Succesfully changed user image")
        return redirect(redirect_url)

    return render(request, 'editprofile.html', {'logged_in':True, 'current_user':request.session['current_user'],
                                                'current_user_id': db.get_users_id_by_username(request.session['current_user'])})
        
@login_required
def getpost(request, post_id):
    return render(request, "post.html", {'logged_in':True, 'current_user':request.session['current_user'],
                                          'current_user_id': db.get_users_id_by_username(request.session['current_user']),
                                          'post':db.get_post_by_post_id(request.session['current_user'], post_id), 'this_url':str(f'/getpost/{post_id}')})

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
    #Get query parameters
    post_id = request.GET.get('post', None)
    redirect_to = request.GET.get('redirect_to', None)

    user = request.session["current_user"]

    #If post is allready liked
    if db.user_liked_post(user, post_id):
        #Dislike post
        db.dislike_post(user, post_id)
    #If post isn't allready liked
    else:
        #Like post
        db.like_post(user, post_id)

        #Add genre to user's interests
        genre = db.get_post_genre(post_id)
        db.add_user_interest(user, genre)

    return redirect('/') if redirect_to == None else redirect(redirect_to)

@login_required
def comment(request):
    if request.method == 'POST':
        content = request.POST['comment_content']
        parrent_id = request.POST['comment_parrent_id']
        db.new_comment(request.session['current_user'], content, parrent_id)
        return JsonResponse({"status": "succes"}, status=200)
    return JsonResponse({"status": "error", "descriprion":"only post method allowed"}, status=500)

def userexists(request):
    user = request.GET.get('user', None)
    if user == None:
        return JsonResponse({"status": "error", "description":"user not provided"}, status=500)
    return JsonResponse({"status": "succes", "user":user, "user_exists":db.user_exists(user)})

@login_required
def post(request):
    user_posting = request.GET.get('user', None)
    content = request.GET.get('content', None)

    if user_posting == request.session['current_user']:
        db.new_post(user_posting, content)

    return redirect('/')

def login(request):
    #First Logout
    logged_out = logout(request)

    #Get "then" query parameter
    then = str(request.GET.get('then', None))

    if request.method == 'POST':
        #Get input values
        username = request.POST['user']
        password = request.POST['password']

        if db.validate_user(username, password):
            request.session["current_user"] = username

            #Redirect to then or /
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
        #Get input values
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
        elif len(username) == 0:
            messages.error(request, "You must set a username")
            return redirect('/register')
        elif ".." in username:
            messages.error(request, "Username cannot contain '..'")
            return redirect('/register')
        elif "/" in username:
            messages.error(request, "Username cannot contain '..'")
            return redirect('/register')
        elif "\\" in username:
            messages.error(request, "Username cannot contain '\\'")
            return redirect('/register')
        elif request.FILES['avatar'].content_type not in allowed_image_type:
            messages.error(request, "Invalid image type")
            return redirect('/register')
        else:
            #Try getting the image
            try:
                a = request.FILES['avatar']
            except:
                messages.error(request, "You must chose an avatar for yourself")
                return redirect('/register')
            
            #Add user and login
            user_id = db.add_user(username, password1)
            request.session["current_user"] = username

            #Load and save the image
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