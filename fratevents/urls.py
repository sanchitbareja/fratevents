from django.conf.urls import patterns, include, url
from fratevents.views import main
from events.models import Event
from clubs.models import Club
from rage.models import Rage

from events.views import getEventsJSON

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fratevents.views.home', name='home'),
    # url(r'^fratevents/', include('fratevents.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',main),
    url(r'^get/events/$',getEventsJSON)
)

