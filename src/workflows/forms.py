from django.forms import ModelForm
from .models import Node
from django import forms

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ['assosiated_role', 'assosiated_team']
        labels = {
            'assosiated_role': ('Role'),
            'assosiated_team': ('Team'),
        }

        help_texts = {
            'assosiated_role': ('Role assosiated with the node'),
            'assosiated_team': ('Team assosiated with the node'),
        }
        

    def __init__(self, *args, **kwargs):
		super(NodeForm, self).__init__(*args, **kwargs)
