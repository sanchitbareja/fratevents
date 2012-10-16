# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from events.models import Event, TYPE_OF_EVENT_CHOICES
import os, time, simplejson
from datetime import datetime, date, timedelta
from django.core.mail import send_mail
from fratevents.settings import EVENT_MASTERS
from rage.models import Rage
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Sum, Count

#return json of everything in database
def getEventsJSON(request):
	results = {'success':False}
	if(request.method == u'POST'):
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

def getFiltersJSON(request):
	results = {'success':False}
	if(request.method == u'POST'):
		filters = {}
		filters_events_count = Event.objects.filter(startTime__gte=datetime(datetime.now().year, datetime.now().month, datetime.now().day)).values('typeOfEvent').annotate(count=Count('typeOfEvent'))
		for afilter in filters_events_count:
			filters[afilter['typeOfEvent']] = afilter['count']
		for afilter in TYPE_OF_EVENT_CHOICES:
			if afilter[0] not in filters.keys():
				filters[afilter[0]] = 0
		results['filters'] = filters
		results['success'] = True
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')

def getFilteredEventsJSON(request, filter_text):
	results = {'success':False}
	if(request.method == u'POST'):
		ordered_events = Event.objects.filter(startTime__gte=datetime(datetime.now().year, datetime.now().month, datetime.now().day), typeOfEvent = filter_text).order_by('startTime')
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

#return json of everything in database - for the iOS app
@csrf_exempt
def getEventsForIOS(request):
	results = {'success':False}
	if(request.method == u'POST'):
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
													'eventDescription':event.description,
													'startTime':event.startTime.ctime(),
													'id':event.id,
													'numberOfRagers':(event.numberOfRagers.values('count')[0]['count'] if(event.numberOfRagers.values('count')) else 0)} for event in events_on_adate)]]
		results['events'] = events_by_date
		results['success'] = True
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')

def eventInfo(request, eventID):
	try:
		event = Event.objects.get(id=eventID)
		similarEvents = Event.objects.exclude(id=event.id).filter(club=event.club, startTime__gte=datetime(datetime.now().year, datetime.now().month, datetime.now().day)).order_by('startTime')
		try:
			rageObject = Rage.objects.get(event__id = event.id)
		except:
			# create a rage object if there is none
			rageObject = Rage(count=0,event=event)
			rageObject.save()
		return render_to_response('eventInfo.html',{'event':event,'rageObject':rageObject,'similarEvents':similarEvents},context_instance=RequestContext(request))
	except:
		raise Http404

def addEvent(request):
	results = {'success':False}
	if(request.method == u'POST'):
		POST = request.POST
		emailBody = "Event Description: "+POST['eventDescription']+"--Event Title: "+POST['eventTitle']+"--When: "+POST['eventWhen']+"--Where: "+POST['eventWhere']+"--Host: "+POST['eventHost']
		send_mail('[CalHaps] Someone wants to add an event!', emailBody, 'caleventsinfo@gmail.com', EVENT_MASTERS, fail_silently=False)
		results['success'] = True
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')