from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import FormInstance
from .routing import get_workflow_user_list

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
