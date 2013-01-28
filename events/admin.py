from django.contrib import admin
from events.models import Event, Location

#register the admin site

class EventAdmin(admin.ModelAdmin):
	list_display = ['title','description','startTime', 'club','typeOfEvent','image', 'location','advertise']

admin.site.register(Event, EventAdmin)
admin.site.register(Location)
