from django.contrib import admin

from .models import FormBlueprint
# Register your models here.

class FormBlueprintAdminModel(admin.ModelAdmin):
	""" Admin Model """

	class Meta:
		model = FormBlueprint

admin.site.register(FormBlueprint, FormBlueprintAdminModel)