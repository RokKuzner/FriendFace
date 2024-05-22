from django.shortcuts import render, redirect
from decorators import login_required
import database as db

@login_required
def home(request):
    current_user_id = db.get_users_id_by_username(request.session["current_user"])

    return render(request, "friendchatindex.html", {"logged_in":True, "current_user":request.session["current_user"],
                                          "current_user_id": current_user_id,
                                          "this_url":str("/"),
                                          "dms":db.get_all_users_dm_companions(current_user_id),
                                          "latest_messages": [db.get_latest_dm_message(dm[2], current_user_id) for dm in db.get_users_dms(current_user_id)]})

@login_required
def dm(request, dm_id):
    current_user_id = db.get_users_id_by_username(request.session["current_user"])

    if ( not db.dm_exists_by_id(dm_id) ) or ( not current_user_id in db.get_dm_members(dm_id)):
        return redirect("/chat")
    
    corresponder_id = db.get_dm_corresponder(dm_id, current_user_id)
    corresponder_username = db.get_username_by_user_id(corresponder_id)
    
    return render(request, "dm.html", {"logged_in":True, "current_user":request.session["current_user"],
                                          "current_user_id": current_user_id,
                                          "this_url":str("/"),
                                          "corresponder_username": corresponder_username,
                                          "coresponed_id": corresponder_id})