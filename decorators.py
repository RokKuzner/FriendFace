from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

def login_required(f):
    def decorated_function(request, *args, **kwargs):
        if "curren_user" in request.session:
            if request.session["curren_user"] != None:
                pass
            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('login'))
        return f(*args, **kwargs)

    return decorated_function