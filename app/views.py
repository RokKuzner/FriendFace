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
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        print(username, password)
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        password = request.POST['password2']
        messages.error(request, "Error")
        print(username, password)
    return render(request, 'register.html')