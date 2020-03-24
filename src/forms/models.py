from django.db import models
from employees.models import Profile, Role
from teams.models import Team
from workflows.models import Workflow

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from employees.models import Profile


class FormBlueprint(models.Model):
    """ Represents a form blueprint """
    #creator of the form is captured in the workflow....
    title = models.CharField(max_length=128)
    workflow = models.OneToOneField(Workflow, on_delete = models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "FB for {}".format(self.workflow.title)



@receiver(post_save, sender=Workflow)
def update_workflow_form(sender, instance, created, **kwargs):
    if created:
        FormBlueprint.objects.create(workflow=instance)
    instance.formblueprint.save()