from django.contrib import admin

from .models import Profile, Role
# Register your models here.

class ProfileAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ["user"]

	search_fields = ["user", "user.email"]

	class Meta:
		model = Profile

admin.site.register(Profile, ProfileAdminModel)


class RoleAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ["role_name"]

	search_fields = ["role_name"]

	class Meta:
		model = Role

admin.site.register(Role, RoleAdminModel)