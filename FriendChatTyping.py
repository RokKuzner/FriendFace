from database import get_dm_members

currenty_typing_by_dm = {}

def start_typing(dm_id:str, user_id:str):
    if user_id not in get_dm_members(dm_id):
        return None

    try:
        currently_typing_in_this_dm = currenty_typing_by_dm[dm_id]

        if user_id not in currently_typing_in_this_dm:
            currenty_typing_by_dm[dm_id].append(user_id)
    except KeyError:
        currenty_typing_by_dm[dm_id] = [user_id]

def stop_typing(dm_id:str, user_id:str):
    try:
        currently_typing_in_this_dm = currenty_typing_by_dm[dm_id]

        if user_id in currently_typing_in_this_dm:
            currenty_typing_by_dm[dm_id].remove(user_id)
    except KeyError:
        pass

def get_currently_typing_in_dm(dm_id:str):
    try:
        currently_typing_in_this_dm = currenty_typing_by_dm[dm_id]
    except KeyError:
        currently_typing_in_this_dm = []

    return currently_typing_in_this_dm