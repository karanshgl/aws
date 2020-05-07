from django.contrib import admin

from .models import Profile, Role
# Register your models here.

class ProfileAdminModel(admin.ModelAdmin):
	""" Admin Model """

	def user_email(obj):
		return obj.user.email.lower()
	user_email.short_description = 'Email'

	def user_first_name(obj):
		return obj.user.first_name
	user_first_name.short_description = 'First Name'

	def user_last_name(obj):
		return obj.user.last_name
	user_last_name.short_description = 'Last Name'


	list_display = ("user", user_email, user_first_name, user_last_name)

	search_fields = ("user__username", "user__email",  )

	class Meta:
		model = Profile

admin.site.register(Profile, ProfileAdminModel)


class RoleAdminModel(admin.ModelAdmin):
	""" Admin Model """

	list_display = ("role_name", )

	search_fields = ("role_name", )

	class Meta:
		model = Role

admin.site.register(Role, RoleAdminModel)