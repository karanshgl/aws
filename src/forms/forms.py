from django.forms import ModelForm
from .models import FormBlueprint
from workflows.models import Workflow
from django import forms

class FormBlueprintForm(ModelForm):
    class Meta:
        model = FormBlueprint
        fields = ['title', 'workflow', 'active']
        labels = {
            'title': ('Title'),
            'workflow': ('Workflow'),
            'active': ('Active')
        }
        help_texts = {
            'title': ('Title of the form'),
            'workflow': ('Select the workflow to be used by this form'),
            'active': ('Form will be visible to others only if active')
        }
        # field_classes = {
        #     'title': forms.CharField(max_length=128, required=True),
        #     'workflow': forms.ChoiceField(required=True),
        # }