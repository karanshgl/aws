from django.db import models
from employees.models import Profile, Role
from teams.models import Team
from workflows.models import Workflow, Node

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
import pymongo
from pymongo import MongoClient

import datetime

from .FormBlueprintParser import *
from employees.models import Profile


class FormBlueprint(models.Model):
    """ Represents a form blueprint """
    #creator of the form is captured in the workflow....
    title = models.CharField(max_length=128)
    workflow = models.OneToOneField(Workflow, on_delete = models.CASCADE)
    active = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return "FB for {}".format(self.workflow.title)

    """get the name of the collection which stores instances of this FB in aws_database"""
    def get_instance_collection_name(self):
        return str(self.id)+"_"+self.workflow.title


    def get_document(self):
        # Returns the blueprint from MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb = collection.find_one({'id': self.id})
        client.close()
        return _fb

    def create_document(self):
        # Creates a collection in MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb = collection.insert_one({'id': self.id})
        client.close()

    def update_document(self, fb):
        #if the FB has already been saved it cannot be updated
        if self.saved==True: return
        fb["date"]= datetime.datetime.now()
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb_id = collection.update_one(
            {"id": self.id},
            {"$set": fb}
        )
        client.close()

    def fetch_preview_html(self):
        #get the form blueprint from mongo and parse it to html then pass return the view
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb = collection.find_one({'id': self.id})
        client.close()
        fb_parser = FormBlueprintParser()
        html=fb_parser.parse_section(_fb, 1)

        return html

    def fetch_section_html(self, section_id):
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb = collection.find_one({'id': self.id})
        client.close()
        fb_parser = FormBlueprintParser()
        html, node_id=fb_parser.parse_section(_fb, section_id)

        return html, node_id

    def create_instance(self, data):
        """this function is called when the instance of the FB is created for the first time"""
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db[self.get_instance_collection_name()]
        collection.insert_one(data)
        client.close()

    def update_instance(self, data):
        """this function is called when someone responds on an instance of the FB """




@receiver(post_save, sender=Workflow)
def update_workflow_form(sender, instance, created, **kwargs):
    if created:
        fb = FormBlueprint.objects.create(workflow=instance)
        # Create a document in MONGO corresponding to this blueprint
        fb.create_document()

    instance.formblueprint.save()



class FormInstance(models.Model):

    blueprint = models.ForeignKey(FormBlueprint, on_delete = models.CASCADE, null = False)
    current_node = models.ForeignKey(Node, on_delete = models.CASCADE, null = False)
    sender = models.ForeignKey(Profile, on_delete = models.CASCADE, null = False)
    active = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False)

    def get_document(self):
        # Returns the blueprint from MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_instances_collection
        _fb = collection.find_one({'id': self.id})
        client.close()
        return _fb

    def create_document(self):
        # Creates a collection in MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_instances_collection
        _fb = collection.insert_one({'id': self.id})
        client.close()


