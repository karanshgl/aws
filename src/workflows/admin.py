from django.contrib import admin

from .models import Node, Workflow
# Register your models here.

class NodeAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ("id", "workflow",  "associated_team", "associated_role",  "prev_node", "next_node", "section_id")
	search_fields = ( "associated_team", "associated_role",)

	class Meta:
		model = Node

admin.site.register(Node, NodeAdminModel)


class WorkflowAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ("id", "title", "creator")
	search_fields = ("title", "creator")

	class Meta:
		model = Workflow

admin.site.register(Workflow, WorkflowAdminModel)