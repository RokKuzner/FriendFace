from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

def login_required(f):
    def decorated_function(request, *args, **kwargs):
        if "current_user" in request.session:
            if request.session["current_user"] is not None:
                pass
            else:
                return redirect('login')
        else:
             return redirect('login')
        return f(request, *args, **kwargs)

    return decorated_function