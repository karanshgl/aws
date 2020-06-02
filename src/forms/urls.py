from django.urls import path, include
from .views import dashboard, fb_all, fb_edit, fb_create, fb_preview, fb_toggle_activation, fi_create, fi_respond, fi_detail, fi_nudge, fb_available_to_instantiate, send_comment
from rest_framework.routers import DefaultRouter
from .api import ListWorkflowUsers

urlpatterns = [
	path('dashboard/', dashboard, name='dashboard',),
	path('fb_all/', fb_all, name='fb_all'),
	path('fb_edit/<int:fb_id>', fb_edit, name='fb_edit'),
	path('fb_preview/<int:fb_id>', fb_preview, name='fb_preview'),
	path('fb_create/', fb_create, name='fb_create'),
	path('fb_toggle_activation/<int:fb_id>', fb_toggle_activation, name='fb_toggle_activation'),
	path('fi_detail/<int:fi_id>', fi_detail, name='fi_detail'),
	path('fi_create/<int:fb_id>', fi_create, name='fi_create'),
	path('fi_respond/<int:fi_id>', fi_respond, name='fi_respond'),
	path('fi_nudge/<int:fi_id>', fi_nudge, name='fi_nudge'),
	path('fb_permitted', fb_available_to_instantiate, name='fb_permitted'),
	path('fi_comment/', send_comment, name='send_comment'),
	path('api/form_instance/<int:fi_id>/users/', ListWorkflowUsers.as_view(), name = 'list_workflow_users'),
]