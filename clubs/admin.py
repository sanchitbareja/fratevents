from django.contrib import admin
from clubs.models import Club

#register the admin site

class ClubAdmin(admin.ModelAdmin):
	list_display = ['name','description','typeOfOrganization','founded','urlPersonal','image']

admin.site.register(Club,ClubAdmin)
