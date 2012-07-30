from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from rage.models import Rage
from events.models import Event
import simplejson

def registerRage(request):
	results = {'success':False}
	if(request.method == 'POST'):
		POST = request.POST
		if POST['id']:
			try:
				existingRage = Rage.objects.get(event__id=POST['id'])
				existingRage.count += 1
				existingRage.save()
				results['numberOfRagers'] = existingRage.count
			except:
				newRage = Rage(count=1,event=Event.objects.get(id=POST['id']))
				newRage.save()
				results['numberOfRagers'] = 1
			results['success'] = True
	json_results = simplejson.dumps(results)
	return HttpResponse(json_results, mimetype='application/json')