from django.db import models
from employees.models import Profile, Role
from teams.models import Team, TeamHasEmployees
from workflows.models import Workflow, Node

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
import pymongo
from pymongo import MongoClient

import datetime

from .FormBlueprintParser import *
from employees.models import Profile

from .routing import get_node_user, get_workflow_user_list

def qdict_to_dict(qdict):
    """Convert a Django QueryDict to a Python dict.

    Single-value fields are put in directly, and for multi-value fields, a list
    of all values is stored at the field's key.

    """
    return {k: v[0] if len(v) == 1 else v for k, v in qdict.lists()}

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
        #update the section ids in the nodes of the workflow
        for i, section in enumerate(fb['sections'], 0):
            node_id = section['node_id']
            node = Node.objects.get(id=node_id)
            node.section_id = i+1 #section_id is 1-indexed
            node.save()
        client.close()

    def fetch_preview_html(self):
        #get the form blueprint from mongo and parse it to html then pass return the view
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db.form_blueprints_collection
        _fb = collection.find_one({'id': self.id})
        client.close()
        fb_parser = FormBlueprintParser()
        html=fb_parser.parse(_fb)

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





@receiver(post_save, sender=Workflow)
def update_workflow_form(sender, instance, created, **kwargs):
    if created:
        fb = FormBlueprint.objects.create(workflow=instance)
        # Create a document in MONGO corresponding to this blueprint
        fb.create_document()

    instance.formblueprint.save()



class FormInstance(models.Model):
    blueprint = models.ForeignKey(FormBlueprint, on_delete = models.CASCADE, null = False, related_name='instances')
    current_node = models.ForeignKey(Node, on_delete = models.CASCADE, null = False)
    sender = models.ForeignKey(Profile, on_delete = models.CASCADE, null = False)
    active = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False)

    def fetch_document(self):
        # Returns the instance from MONGO
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db[self.blueprint.get_instance_collection_name()]
        document = collection.find_one({'id': self.id})
        client.close()
        return document

    def create_document(self, data):
        # Creates the instance in MONGO
        responses = {'responses':[]}
        responses['id'] = self.id
        data['date_time'] = self.creation_time
        data['user'] = self.sender.user.email
        data['node_id'] = self.current_node.id
        # data['section_id'] = self.current_node.sec
        responses['responses'].append(data)
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db[self.blueprint.get_instance_collection_name()]
        collection.insert_one(responses)
        client.close()

    def add_response(self, data):
        #add meta information to the data
        data['date_time'] = datetime.datetime.now()
        data['user'] = self.sender.user.email
        data['node_id'] = self.current_node.id
        data = qdict_to_dict(data)# convert q_dict to dict
        #get the doc from mongo
        client = MongoClient(settings.MONGO_IP, settings.MONGO_PORT)
        db = client.aws_database
        collection = db[self.blueprint.get_instance_collection_name()]
        document = collection.find_one({'id': self.id})
        #update the responses array and the current response
        document['responses'].append(data)
        collection.update_one(
            {'id': self.id},
            {'$set': document}
        )
        client.close()

    def fetch_responses(self):
        document = self.fetch_document()
        return document['responses']

    """send this instance to the next node"""
    def send_forward(self, sender):
        # Create an instance in form notifcation

        the_sender = sender.teamhasemployees
        notification, created = FormNotification.objects.get_or_create(user = the_sender, form_instance = self) 
        notification.status = 'F'
        notification.save()

        if self.current_node.next_node:
            next_node = self.current_node.next_node
            # Get Receiver
            receiver = get_node_user(next_node, sender)
            the_receiver = receiver.teamhasemployees

            # Send notification
            notification, created = FormNotification.objects.get_or_create(user = the_receiver, form_instance = self)
            notification.status = 'N'
            notification.save()

            self.current_node = next_node
            return True

        # FINAL NODE
        self.active = False
        return False
    """send this instance to the prev node"""
    def send_backward(self):
        if self.current_node.prev_node:
            self.current_node = self.current_node.prev_node
            return True 
        return False

    def is_user_in_workflow(self, user):
        # Checks whether the user is part of the workflow or not
        user_list = get_workflow_user_list(self)

        return user in user_list

    def is_user_current_node(self, user):
        # Checks whether the user is the current node or not
        current_node = self.current_node
        blueprint = self.blueprint
        workflow = blueprint.workflow
        head = Workflow.objects.get(workflow = workflow, prev_node = None)

        sender = self.sender

        # IF CURRENT NODE IS HEAD
        if current_node == head:
            return user == sender

        it_node = head

        while it_node != current_node:
            it_node = it_node.next_node
            receiver = get_node_user(it_node, sender)
            sender = receiver

        # Now the sender is the current node user
        return user == sender
        


class FormNotification(models.Model):
    # Manages form notifications

    user = models.ForeignKey(TeamHasEmployees, on_delete = models.CASCADE, null = False, blank = False) # User who gets notifcation
    form_instance = models.ForeignKey(FormInstance, on_delete = models.CASCADE, null = False, blank = False) # Corresponding form instance

    STATUS_CHOICES = (
            ('F', 'Forwarded'),
            ('B', 'Sent Back for comments'),
            ('N', 'No Action Taken')
        )

    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = 'N')


    def __str__(self):
        return '{} : {}'.format(self.user, self.form_instance)


