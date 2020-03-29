from django.urls import path, include
from .views import create_workflow

urlpatterns = [
	path('create/', create_workflow, name='create_workflow'),
]