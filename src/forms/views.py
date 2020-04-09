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

from .FormBlueprintParser import *


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
        print(fb)
        fb["date"]= datetime.datetime.now()
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb_id = collection.insert_one(fb).inserted_id
        client.close()
        #mark form as saved
        _fb = FormBlueprint.objects.get(pk=fb["id"])
        _fb.saved = True
        _fb.save()

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
    client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
    db = client.aws_database
    collection = db.form_blueprints_collection
    _fb = collection.find_one({'id': fb_id})
    client.close()
    fb_parser = FormBlueprintParser()
    html=fb_parser.parse(_fb)
    
    context = {
        'html':html
    }
    return render(request, 'forms/fb_preview.html', context = context)