from django.db import models
from employees.models import Profile, Role
from teams.models import Team
from workflows.models import Workflow, Node

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
import pymongo
from pymongo import MongoClient


# Create your models here.
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


    def get_collection(self):
        # Returns the blueprint from MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb = collection.find_one({'id': self.id})
        client.close()
        return _fb

    def create_collection(self):
        # Creates a collection in MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb = collection.insert_one({'id': self.id})
        client.close()




@receiver(post_save, sender=Workflow)
def update_workflow_form(sender, instance, created, **kwargs):
    if created:
        fb = FormBlueprint.objects.create(workflow=instance)
        # Create a collection in MONGO
        fb.create_collection()

    instance.formblueprint.save()



class FormInstance(models.Model):

    blueprint = models.ForeignKey(FormBlueprint, on_delete = models.CASCADE, null = False)
    current_node = models.ForeignKey(Node, on_delete = models.CASCADE, null = False)
    sender = models.ForeignKey(Profile, on_delete = models.CASCADE, null = False)
    active = models.BooleanField(default=False)


    def get_collection(self):
        # Returns the blueprint from MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_instances_collection
        _fb = collection.find_one({'id': self.id})
        client.close()
        return _fb

    def create_collection(self):
        # Creates a collection in MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_instances_collection
        _fb = collection.insert_one({'id': self.id})
        client.close()


