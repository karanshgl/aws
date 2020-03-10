from django.contrib import admin

from .models import TeamHasEmployees, Team
# Register your models here.

class TeamHasEmployeesAdminModel(admin.ModelAdmin):
	""" Admin Model """

	class Meta:
		model = TeamHasEmployees

admin.site.register(TeamHasEmployees, TeamHasEmployeesAdminModel)


class TeamAdminModel(admin.ModelAdmin):
	""" Admin Model """

	class Meta:
		model = Team

admin.site.register(Team, TeamAdminModel)