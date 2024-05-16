from django.shortcuts import render
from decorators import login_required
import database as db

@login_required
def home(request):
    current_user_id = db.get_users_id_by_username(request.session['current_user'])

    print(db.get_all_users_dm_companions(current_user_id))


    return render(request, 'friendchatindex.html', {'logged_in':True, 'current_user':request.session['current_user'],
                                          'current_user_id': current_user_id,
                                          'this_url':str('/'),
                                          "dms":db.get_all_users_dm_companions(current_user_id)})