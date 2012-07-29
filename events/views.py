# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from events.models import Event
import os, time, simplejson

#return json of everything in database
def getEventsJSON(request):
	print "debug 1"
	results = {'success':False}
	print "debug 2"
	if(request.method == u'GET'):
		print "debug 3"
		GET = request.GET
		print "debug 4"
		events = Event.objects.all()
		print "debug 5"
		results['success'] = True
		print "debug 6"
		to_serialize_events = {}
		print "debug 7"
		for event in events:
			to_serialize_events[event.id] = {'title':event.title,'lat':float(event.lat),'lng':float(event.lng),'host':event.club.name,'where':event.where,'startTime':time.mktime(event.startTime.timetuple()),'endTime':time.mktime(event.endTime.timetuple())}
		results['events'] = to_serialize_events
		print "debug 8"
	print results
	json_results = simplejson.dumps(results)
	print "debug 9"
	return HttpResponse(json_results, mimetype='application/json')