from django.contrib import admin
from events.models import Event

#register the admin site
admin.site.register(Event)
