from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    context ={

    }
    return render(request, 'forms/dashboard.html', context=context)

@login_required
def create(request):
    context={

    }
    return render(request, 'forms/create.html', context=context)