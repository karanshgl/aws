from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.filters import SearchFilter



from .serializers import TeamSerializer
from .models import Team

class TeamViewSet(viewsets.ModelViewSet):
	
	queryset = Team.objects.all()
	serializer_class = TeamSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('team_name',)
	search_fields = ('team_name',)


