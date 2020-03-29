from django.conf import settings
from rest_framework import serializers
from . import models

class RoleSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Role
		fields = '__all__' 
