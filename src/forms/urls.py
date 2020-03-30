from django.urls import path, include
from .views import dashboard, fb_edit, fb_create

urlpatterns = [
	path('dashboard/', dashboard, name='forms_dashboard'),
	path('fb_edit/<int:fb_id>', fb_edit, name='forms_blueprint_edit'),
	path('fb_create/', fb_create),
]