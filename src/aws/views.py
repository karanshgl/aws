from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages

from teams.models import TeamHasEmployees


# @login_required
def home(request):
    return render(request, 'aws/home/home.html')

@login_required
def profile(request):
    try:
        the_instance = TeamHasEmployees.objects.get(employee= request.user.profile)

        user_role=the_instance.role
        user_team=the_instance.team
    except:
        user_role="NA"
        user_team="NA"
    
    # TODO : Add info whether user has blueprint creation permission or not, depends on TeamsHasPermission and EmployeeHasPermission in workflows.models
    # TODO : Add first name, last name if avaiable in user.profile
    context={
        "user": request.user,
        "role": user_role,
        "team": user_team
    }
    print("in profile: role: "+str(user_role))
    return render(request, 'aws/accounts/profile.html', context=context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'aws/accounts/password_changed.html', {})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'aws/accounts/change_password.html', {
        'form': form
    })



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})