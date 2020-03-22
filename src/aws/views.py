from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required
def home(request):
    return render(request, 'aws/home/home.html')