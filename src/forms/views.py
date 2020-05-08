from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import FormBlueprintForm
from .models import FormBlueprint
from workflows.models import Workflow
import json
import pymongo
from pymongo import MongoClient
from django.conf import settings
import datetime




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
    workflow = Workflow.objects.get(formblueprint = fb_object)
    #check if the creator is the one currently logged in
    if request.user.profile!=fb_object.workflow.creator:
        context={
            'title': 'Unauthorised Access',
            'message': 'Unauthorised Access: Only the creator of the form is allowed to access this page'
        }
        return render(request, 'message.html', context=context)
    if fb_object.saved==True:
        context={
            'title': 'Unauthorised Access',
            'message': 'Unauthorised Access: A form blueprint once saved cannot be edited'
        }
        return render(request, 'message.html', context=context)
    context = {
        'fb_object': fb_object,
        'workflow_nodes': workflow.get_flow(),
    }
    return render(request, 'forms/fb_edit.html', context=context)

@login_required
def fb_toggle_activation(request, fb_id):#fb is for form blueprint
    fb_object = FormBlueprint.objects.get(pk=fb_id)
    #check if the creator is the one currently logged in
    if request.user.profile!=fb_object.workflow.creator:
        context={
            'title': 'Unauthorised Access',
            'message': 'Unauthorised Access: Only the creator of the form is allowed to toggle the activation'
        }
        return render(request, 'message.html', context=context)
    #toggle the active attribute and save
    if fb_object.active==True:fb_object.active=False
    else: fb_object.active=True
    fb_object.save()

    return redirect('forms_blueprint_dashboard')


def fb_create(request):
    if request.method=='POST':
        fb = dict(json.loads(request.POST['fb']))#fb is the form_blueprint
        fb_object = FormBlueprint.objects.get(id=fb["id"])

        if fb_object.saved==True:
            context={
                'title': 'Unauthorised Access',
                'message': 'Unauthorised Access: A form blueprint once saved cannot be edited'
            }
        fb_object.update_document(fb)

        #mark form as saved
        fb_object.saved = True
        fb_object.save()

    return HttpResponse('Successfull')

@login_required
def fb_preview(request, fb_id):
    fb_object = FormBlueprint.objects.get(pk=fb_id)
    if fb_object.saved==False:
        context={
            'title': 'Unauthorised Access',
            'message': 'Unauthorised Access: A form blueprint has to be saved to be previewed'
        }
        return render(request, 'message.html', context=context)
    #get the form blueprint from mongo and parse it to html then pass return the view
    preview_html = fb_object.fetch_preview_html()

    context = {
        'preview_html':preview_html
    }
    return render(request, 'forms/fb_preview.html', context = context)

@login_required
def fi_create(request, fb_id):
    #get the section of the form relevant to this person and render that section
    #for now assuming that it is the first section which is relevant for creation of the form
    fb_object = FormBlueprint.objects.get(id=fb_id)
    section_id = 1
    section_html, node_id = fb_object.fetch_section_html(section_id)
    if request.method=="POST":
        #save the  instance in MONGO in the relevant collection
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        fb_object.create_instance(data)
        return HttpResponse("Form Instance Created")
    else:
        #add the form html tag and the submit button to the section html
        context = {
            'section_html':section_html
        }
        return render(request, 'forms/fi_create.html', context = context)


@login_required
def fi_respond(request):
    pass