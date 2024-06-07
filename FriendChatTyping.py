from database import get_dm_members, get_utc_timestamp, get_username_by_user_id

currently_typing_by_dm = {}

"""
User typing object {"user_id":"923Esdvf8013aD6", "user_username":"a random username", "last_typing_time":2124134.39867}
"""

def start_typing(dm_id:str, user_id:str):

    #Checks if the user is in the dm that was provided
    if user_id not in get_dm_members(dm_id):
        return None

    if is_user_typing_in_dm(dm_id, user_id) == False:
        #If the user isn't allready typing create and add the user object to currently_typing_by_dm
        try:
            currently_typing_by_dm[dm_id].append({"user_id":user_id, "user_username":get_username_by_user_id(user_id), "last_typing_time":float(get_utc_timestamp())})
        except KeyError:
            currently_typing_by_dm[dm_id] = [{"user_id":user_id, "user_username":get_username_by_user_id(user_id), "last_typing_time":float(get_utc_timestamp())}]
    else:
        #If the user is allready typing update the time of last typing
        get_user_typing_object_in_dm(dm_id, user_id)["last_typing_time"] = float(get_utc_timestamp())

def stop_typing(dm_id:str, user_id:str):

    #If user is typing
    if is_user_typing_in_dm(dm_id, user_id):
        currently_typing_by_dm[dm_id].remove(get_user_typing_object_in_dm(dm_id, user_id)) #Remove user from list of users typing

def get_currently_typing_in_dm(dm_id:str):
    try:
        remove_users_not_typing(dm_id) #Remove users that haven't been typing for a while from the array

        return currently_typing_by_dm[dm_id] #Return the array of users currently typing
    except KeyError:
        return [] #Return empty array if the provided dm isn't in the currently_typing_by_dm set

def is_user_typing_in_dm(dm_id:str, user_id:str):
    if get_user_typing_object_in_dm(dm_id, user_id):
        return True
    return False
    
def get_user_typing_object_in_dm(dm_id:str, user_id:str):
    try:
        currently_typing_in_this_dm = currently_typing_by_dm[dm_id] #Get the array of users currently typing in provided dm

        for user_typing in currently_typing_in_this_dm:
            if user_typing["user_id"] == user_id:
                return user_typing #Return the user object
    except KeyError:
        pass

    return []

def remove_users_not_typing(dm_id:str, not_typing_treshold=3):
    #Get the users currently typing in provided dm
    try:
        users_typing = currently_typing_by_dm[dm_id]
    except KeyError:
        users_typing = []

    #Check if each user is typing longer then not_typing_treshold seconds
    for user_typing in users_typing:
        if float(get_utc_timestamp()) - user_typing["last_typing_time"] >= not_typing_treshold:
            #Remove the user not typing longer than not_typing_treshold seconds from the array of users typing in provided dm
            stop_typing(dm_id, user_typing["user_id"])