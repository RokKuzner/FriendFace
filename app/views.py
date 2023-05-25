from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'index.html')