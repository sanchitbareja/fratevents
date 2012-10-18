from django.conf.urls import patterns, include, url
from fratevents.views import main, feedbackForm
from rage.views import registerRage
from events.views import getEventsJSON, eventInfo, addEvent, getEventsForIOS, getFiltersJSON, getFilteredEventsJSON
from clubs.views import getClubInfoJSON
from fratevents import settings

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
    url(r'^get/events/$',getEventsJSON),
    url(r'^get/filters/$',getFiltersJSON),
    url(r'^get/filters/(.[A-Za-z0-9]+)/$',getFilteredEventsJSON),
    url(r'^get/ios/events/$',getEventsForIOS),
    url(r'^rage/$',registerRage),
    url(r'^get/club/$',getClubInfoJSON),
    url(r'^feedback/$',feedbackForm),
    url(r'^event/(.+)/$',eventInfo),
    url(r'^add/event/$',addEvent),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL, 'show_indexes':True}),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
)

