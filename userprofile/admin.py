from django.contrib import admin
from userprofile.models import UserProfile

#register the admin site
admin.site.register(UserProfile)