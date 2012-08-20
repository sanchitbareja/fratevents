from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import os, time, simplejson

def main(request):
	print request.COOKIES
	if request.COOKIES.get("joyride"):
		print "1"
		returnValue = render_to_response('index.html', {"takeTour":"false"}, context_instance=RequestContext(request))
	else:
		print "2"
		returnValue = render_to_response('index.html', {"takeTour":"true"}, context_instance=RequestContext(request))
		returnValue.set_cookie("joyride",value="true")
	return returnValue

def feedbackForm(request):
	results = {'success':False}
	if(request.method == u'POST'):
		POST = request.POST
		send_mail('[CalHaps] Someone just left you a feedback!', POST['feedback'], 'caleventsfrat@gmail.com', ['sanchitbareja@gmail.com','hahardikagrawal@gmail.com'], fail_silently=False)
		results['success'] = True
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')