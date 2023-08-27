from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from decorators import login_required

# Create your views here.
@login_required
def home(request):
    if "curren_user" in request.session:
        if request.session["curren_user"] != None:
            pass
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')