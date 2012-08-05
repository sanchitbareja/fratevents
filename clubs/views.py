# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from clubs.models import Club
import os, time, simplejson
from datetime import datetime, date

#return json of everything in database
def getClubInfoJSON(request):
	results = {'success':False}
	try:
		if(request.method == u'POST'):
			POST = request.POST
			print POST['clubID']
			club = Club.objects.get(id=POST['clubID'])
			print club
			results['id'] = club.id
			results['name'] = club.name
			print "debug 1"
			results['description'] = club.description
			print "debug 2"
			results['typeOfOrganization'] = club.typeOfOrganization
			print "debug 3"
			results['founded'] = club.founded
			print "debug 4"
			results['numberOfChapter'] = club.numberOfChapter
			print "debug 5"
			results['numberOfMembers'] = club.numberOfMembers
			print "debug 6"
			results['urlPersonal'] = club.urlPersonal
			print "debug 7"
			results['urlBerkeley'] = club.urlBerkeley
			print "debug 8"
			results['image'] = club.image
			print "debug 9"

			results['success'] = True
		print "debug 9"
	except:
		pass
	print results
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')
