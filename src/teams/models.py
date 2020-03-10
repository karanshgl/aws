from django.db import models
from employees.models import Profile, Role
# Create your models here.

class Team(models.Model):
    """ Represents a team in an organization """
    team_name = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    parent = models.ForeignKey('Team', on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.team_name



class TeamHasEmployees(models.Model):
    """ Represents a Relationship b/w Team and Employee (Profile) """

    role = models.ForeignKey(Role, on_delete = models.CASCADE, null = False)
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null = False)
    employee = models.ForeignKey(Profile, on_delete = models.CASCADE, null = False)

    def __str__(self):
        return "{} {}: {}".format(self.team, self.role, self.employee)
