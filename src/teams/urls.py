from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .api import TeamViewSet
router = DefaultRouter()
router.register(r'team', TeamViewSet)


urlpatterns = [
	# path('dashboard/', dashboard, name='dashboard'),
	path('api/', include(router.urls)),
]