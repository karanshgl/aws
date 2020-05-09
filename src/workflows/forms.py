from django.forms import ModelForm
from .models import Node
from django import forms

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ['associated_role', 'associated_team']
        labels = {
            'associated_role': ('Role'),
            'associated_team': ('Team'),
        }

        help_texts = {
            'associated_role': ('Role associated with the node'),
            'associated_team': ('Team associated with the node'),
        }
        

    def __init__(self, *args, **kwargs):
		super(NodeForm, self).__init__(*args, **kwargs)
