from django.shortcuts import render
from decorators import login_required
import database as db

@login_required
def home(request):
    return render(request, 'friendchatindex.html', {'logged_in':True, 'current_user':request.session['current_user'],
                                          'current_user_id': db.get_users_id_by_username(request.session['current_user']),
                                          'this_url':str('/')})