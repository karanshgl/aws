from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import FormBlueprintForm
from .models import FormBlueprint


# Create your views here.
@login_required
def dashboard(request):
    context ={
        'form_blueprints':FormBlueprint.objects.all()
    }
    return render(request, 'forms/dashboard.html', context=context)

@login_required
def fb_edit(request, fb_id):#fb is for form blueprint
    fb_object = FormBlueprint.objects.get(pk=fb_id)
    #check if the creator is the one currently logged in
    if request.user.profile!=fb_object.workflow.creator:
        context={
            'title': 'Unauthorised Access',
            'message': 'Unauthorised Access: Only the creator of the form is allowed to access this page'
        }
        return render(request, 'message.html', context=context)
    context = {
        'fb_object': fb_object,
    }
    return render(request, 'forms/fb_edit.html', context=context)

def fb_create(request):
    print(request)
    print(request.POST['fb'])

    return HttpResponse('Successfull')