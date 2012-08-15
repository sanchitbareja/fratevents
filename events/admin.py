from django.contrib import admin
from events.models import Event, Location

#register the admin site
admin.site.register(Event)
admin.site.register(Location)
