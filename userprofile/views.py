from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
import os, time, simplejson
from datetime import datetime, date, timedelta
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Sum, Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def login_view(request):
	results = {"success":False,"login_type":"customer"}
	if(request.method == u'POST'):
		print request.POST
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				print "Successfully logged in!"
				if Group.objects.get(name="club") in user.groups.all():
					results["login_type"] = "club"
				results["success"] = True
				return HttpResponse(simplejson.dumps(results), mimetype="application/json")
			else:
				print "account disabled logged in"
				return HttpResponse(simplejson.dumps(results), mimetype="application/json")
		else:
			print "Failed login"
			return HttpResponse(simplejson.dumps(results), mimetype="application/json")
	else:
		return render_to_response("clubLogin.html", context_instance = RequestContext(request))