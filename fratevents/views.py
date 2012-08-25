from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import os, time, simplejson
from datetime import datetime, timedelta, time
from fratevents.settings import EVENT_MASTERS

def main(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

def feedbackForm(request):
	results = {'success':False}
	if(request.method == u'POST'):
		POST = request.POST
		send_mail('[CalHaps] Someone just left you a feedback!', POST['feedback'], 'caleventsinfo@gmail.com', EVENT_MASTERS, fail_silently=False)
		results['success'] = True
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')