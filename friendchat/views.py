from django.shortcuts import render, redirect
from decorators import login_required
import database as db

@login_required
def home(request):
    current_user_id = db.get_users_id_by_username(request.session["current_user"])

    return render(request, "friendchat/friendchatindex.html", {"logged_in":True, "current_user":request.session["current_user"],
                                          "current_user_id": current_user_id,
                                          "this_url":str("/"),
                                          "dms":[db.get_dm_preview(dm[2], current_user_id) for dm in db.get_latest_active_dms_by_user(current_user_id)]})

@login_required
def dm(request, dm_id):
    current_user_id = db.get_users_id_by_username(request.session["current_user"])

    if ( not db.dm_exists_by_id(dm_id) ) or ( not current_user_id in db.get_dm_members(dm_id)):
        return redirect("/chat")
    
    corresponder_id = db.get_dm_corresponder(dm_id, current_user_id)
    corresponder_username = db.get_username_by_user_id(corresponder_id)
    
    return render(request, "friendchat/dm.html", {"logged_in":True, "current_user":request.session["current_user"],
                                          "current_user_id": current_user_id,
                                          "this_url":str("/"),
                                          "corresponder_username": corresponder_username,
                                          "coresponed_id": corresponder_id,
                                          "messages": db.get_dm_messages(dm_id),
                                          "dm_id": dm_id})

@login_required
def new_dm(request):
    current_user_id = db.get_users_id_by_username(request.session["current_user"])

    if request.method == 'GET':
        return render(request, "friendchat/new_dm.html", {"logged_in":True, "current_user":request.session["current_user"],
                                          "current_user_id": current_user_id,
                                          "this_url":str("/")})
    

    user_username_to_add = request.POST["user-username-to-add"]
    if db.user_exists(user_username_to_add) == False or user_username_to_add == request.session["current_user"]:
        return redirect("/chat/new")

    user_id_to_add = db.get_users_id_by_username(user_username_to_add)

    if db.dm_exists_by_users(current_user_id, user_id_to_add):
        return redirect(f"/chat/dm/{db.get_dm_id_by_members(current_user_id, user_id_to_add)}")
    
    new_dm_id = db.create_dm(current_user_id, user_id_to_add)
    return redirect(f"/chat/dm/{new_dm_id}")