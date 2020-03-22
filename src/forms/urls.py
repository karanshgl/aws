from django.urls import path, include
from .views import dashboard, create

urlpatterns = [
	path('dashboard/', dashboard, name='forms_dashboard'),
	path('create/', create, name='forms_create')
]