from django.urls import path, include
from .views import dashboard, fb_edit

urlpatterns = [
	path('dashboard/', dashboard, name='forms_dashboard'),
	path('fb_edit/<int:fb_id>', fb_edit, name='forms_blueprint_edit')
]