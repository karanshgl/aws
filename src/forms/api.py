from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import FormInstance
from .routing import get_workflow_user_list
from teams.models import TeamHasEmployees, Team
from employees.models import Role

class ListWorkflowUsers(APIView):
    """
    For a given form instance, return the list of user profiles
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, fi_id, format=None):
        """
        Return a list of all users.
        """
        fi = FormInstance.objects.get(pk = fi_id)
        user_list = get_workflow_user_list(fi, fi.current_node)

        queryset = [{
        'id': user.id,
        'username': user.user.username
        } for user in user_list]

        return Response(queryset)


class ListTeamsHavingRole(APIView):
    """
    For a given role, return the list of teams having that role
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, role_name, format=None):
        """
        Return a list of all teams.
        """
        role_name = role_name.replace("-"," ")
        if(role_name == "None"):
            teams = Team.objects.all()
            queryset = [{
                'id': team.id,
                'team': team.team_name
            } for team in teams]

        else:
            teams = TeamHasEmployees.objects.filter(role__role_name = role_name)
            queryset = [{
                'id': team.team.id,
                'team': team.team.team_name
            } for team in teams]

        return Response(queryset)


class ListRolesInTeam(APIView):
    """
    For a given team, return the list of roles in that team
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, team_name, format=None):
        """
        Return a list of all teams.
        """
        team_name = team_name.replace("-"," ")
        if(team_name == "None"):
            roles = Role.objects.all()
            queryset = [{
                'id': role.id,
                'role': role.role_name
            } for role in roles]

        else:
            teams = TeamHasEmployees.objects.filter(team__team_name = team_name)
            queryset = [{
                'id': role.role.id,
                'role': role.role.role_name
            } for role in teams]

        return Response(queryset)
