from django.urls import path, include
from .views import dashboard, fb_edit, fb_create, fb_preview, fb_toggle_activation

urlpatterns = [
	path('dashboard/', dashboard, name='forms_blueprint_dashboard'),
	path('fb_edit/<int:fb_id>', fb_edit, name='forms_blueprint_edit'),
	path('fb_preview/<int:fb_id>', fb_preview, name='forms_blueprint_preview'),
	path('fb_create/', fb_create, name='forms_blueprint_create'),
	path('fb_toggle_activation/<int:fb_id>', fb_toggle_activation, name='forms_blueprint_toggle_activation'),
]