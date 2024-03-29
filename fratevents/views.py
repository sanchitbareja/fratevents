from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import os, time, simplejson
from datetime import datetime, timedelta, time
from fratevents.settings import EVENT_MASTERS

#TESTING FACEBOOK INTEGRATION
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.utils import setting


def main(request):
    if request.user.is_authenticated():
        print request.user
        ctx = {'logged_in': True, 'user': request.user}
    else:
        ctx = {'logged_in': False}
    return render_to_response('index.html', ctx, context_instance=RequestContext(request))

def feedbackForm(request):
    results = {'success':False}
    if(request.method == u'POST'):
        POST = request.POST
        send_mail('[CalHaps] Someone just left you a feedback!', POST['feedback']+" REPLY TO EMAIL: "+POST['replyToEmail'], 'caleventsinfo@gmail.com', EVENT_MASTERS, fail_silently=False)
        results['success'] = True
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')

#facebook integration
@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('done.html', ctx, RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')
