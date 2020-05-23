from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
	""" A Model Representing a User Profile"""

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.user.username


class Role(models.Model):
	""" Represents a Role """

	role_name = models.CharField(max_length = 255, unique = True, null = False, blank = False)
	default_head = models.BooleanField(default=False) # Tells us whether the role is a default head in the team or not

	def __str__(self):
		return self.role_name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()