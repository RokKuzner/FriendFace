from database import get_dm_members, get_utc_timestamp, get_username_by_user_id

currently_typing_by_dm = {}

"""
User typing object {"user_id":"923Esdvf8013aD6", "user_username":"a random username", "last_typing_time":2124134.39867}
"""

def start_typing(dm_id:str, user_id:str):

    if user_id not in get_dm_members(dm_id):
        return None

    if is_user_typing_in_dm(dm_id, user_id) == False:
        try:
            currently_typing_by_dm[dm_id].append({"user_id":user_id, "user_username":get_username_by_user_id(user_id), "last_typing_time":float(get_utc_timestamp())})
        except KeyError:
            currently_typing_by_dm[dm_id] = [{"user_id":user_id, "user_username":get_username_by_user_id(user_id), "last_typing_time":float(get_utc_timestamp())}]
    else:
        get_user_typing_object_in_dm(dm_id, user_id)["last_typing_time"] = float(get_utc_timestamp())

def stop_typing(dm_id:str, user_id:str):

    if is_user_typing_in_dm(dm_id, user_id):
        currently_typing_by_dm[dm_id].remove(get_user_typing_object_in_dm(dm_id, user_id))

def get_currently_typing_in_dm(dm_id:str):
    try:
        remove_users_not_typing(dm_id)

        return currently_typing_by_dm[dm_id]
    except KeyError:
        return []

def is_user_typing_in_dm(dm_id:str, user_id:str):
    return True if get_user_typing_object_in_dm(dm_id, user_id) else False
    
def get_user_typing_object_in_dm(dm_id:str, user_id:str):
    try:
        currently_typing_in_this_dm = currently_typing_by_dm[dm_id]

        for user_typing in currently_typing_in_this_dm:
            if user_typing["user_id"] == user_id:
                return user_typing
    except KeyError:
        pass

    return []

def remove_users_not_typing(dm_id:str, not_typing_treshold=3):
    try:
        users_typing = currently_typing_by_dm[dm_id]
    except KeyError:
        users_typing = []

    for user_typing in users_typing:
        if float(get_utc_timestamp()) - user_typing["last_typing_time"] >= not_typing_treshold:
            stop_typing(dm_id, user_typing["user_id"])