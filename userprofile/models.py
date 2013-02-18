from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from fratevents.settings import AWS_UPLOAD_DESTINATION

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    # accepted_eula = models.BooleanField()
    birthday = models.DateField()
    profilePic = models.TextField(null = True, blank = True, default=AWS_UPLOAD_DESTINATION+"unknown_profile.png")
