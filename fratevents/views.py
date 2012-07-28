from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect

def main(request):
	return render_to_response('index.html',RequestContext(request))