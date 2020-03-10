from django.contrib import admin

from .models import Node, Workflow
# Register your models here.

class NodeAdminModel(admin.ModelAdmin):
	""" Admin Model """

	class Meta:
		model = Node

admin.site.register(Node, NodeAdminModel)


class WorkflowAdminModel(admin.ModelAdmin):
	""" Admin Model """

	class Meta:
		model = Workflow

admin.site.register(Workflow, WorkflowAdminModel)