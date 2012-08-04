# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from events.models import Event
import os, time, simplejson
from datetime import datetime, date

#return json of everything in database
def getEventsJSON(request):
	results = {'success':False}
	if(request.method == u'GET'):
		GET = request.GET
		print "debug 7"
		ordered_events = Event.objects.order_by('startTime')
		unique_dates = []
		for event in ordered_events:
			if event.startTime.date() not in unique_dates:
				unique_dates.append(event.startTime.date())
		events_by_date = []
		print "debug 7.5"
		for adate in unique_dates:
			events_on_adate = Event.objects.filter(startTime__year=adate.year, startTime__month=adate.month, startTime__day=adate.day).order_by('startTime')
			events_by_date += [[adate.ctime(),list({'title':event.title,
													'lat':float(event.lat),
													'lng':float(event.lng),
													'host':event.club.name,
													'where':event.where,
													'startTime':event.startTime.ctime(),
													'id':event.id,
													'numberOfRagers':(event.numberOfRagers.values('count')[0]['count'] if(event.numberOfRagers.values('count')) else 0)} for event in events_on_adate)]]
		results['events'] = events_by_date
		results['success'] = True
		print "debug 8"
	print results
	json_results = simplejson.dumps(results)
	print "debug 9"
	return HttpResponse(json_results, mimetype='application/json')