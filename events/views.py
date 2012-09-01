# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from events.models import Event
import os, time, simplejson
from datetime import datetime, date, timedelta
from django.core.mail import send_mail
from fratevents.settings import EVENT_MASTERS

#return json of everything in database
def getEventsJSON(request):
	results = {'success':False}
	if(request.method == u'GET'):
		GET = request.GET
		ordered_events = Event.objects.filter(startTime__gte=datetime(datetime.now().year, datetime.now().month, datetime.now().day)).order_by('startTime')
		unique_dates = []
		for event in ordered_events:
			if event.startTime.date() not in unique_dates:
				unique_dates.append(event.startTime.date())
		events_by_date = []
		for adate in unique_dates:
			events_on_adate = Event.objects.filter(startTime__year=adate.year, startTime__month=adate.month, startTime__day=adate.day).order_by('startTime')
			events_by_date += [[adate.ctime(),list({'title':event.title,
													'lat':float(event.location.lat),
													'lng':float(event.location.lng),
													'host':event.club.name,
													'hostid':event.club.id,
													'image':event.club.image,
													'where':event.location.name,
													'eventDescription':event.description[0:40],
													'startTime':event.startTime.ctime(),
													'id':event.id,
													'numberOfRagers':(event.numberOfRagers.values('count')[0]['count'] if(event.numberOfRagers.values('count')) else 0)} for event in events_on_adate)]]
		results['events'] = events_by_date
		results['success'] = True
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')

def eventInfo(request, eventName):
	print eventName
	event = Event.objects.filter(title=eventName)[0]
	return render_to_response('eventInfo.html',{'event':event},context_instance=RequestContext(request))

def addEvent(request):
	results = {'success':False}
	if(request.method == u'POST'):
		print "1"
		POST = request.POST
		print "2"
		send_mail('[CalHaps] Someone wants to add an event!', POST['eventInfo'], 'caleventsinfo@gmail.com', EVENT_MASTERS, fail_silently=False)
		print "3"
		results['success'] = True
		print "4"
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')