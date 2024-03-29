from social_auth.backends.facebook import FacebookBackend
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
from urllib2 import urlopen

def create_user_profile(backend, details, response, social_user, uid, user, *args, **kwargs):
    # create user profile here.
    None

def get_user_profile_pic(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    print response
    print backend
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/%s/picture?type=large" % response['id']
 
    if url:
        print "url"
        print url
        profile_pic = urlopen(url).read()
        fout = open(response['id'], "wb") #filepath is where to save the image
        fout.write(profile_pic)
        fout.close()
        default_storage.save(str(response['id'])+'.jpg',File(open(response['id'],'rwb')))
    

def get_user_events(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/"+str(response['id'])+"/events?access_token="+str(response['access_token'])
        print urlopen(url).read()

def get_user_network(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/fql?q=select%20affiliations%20from%20user%20where%20uid="+str(response['id'])+"&access_token="+response['access_token']
        print urlopen(url).read()

def get_user_pages(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/fql?q=select%20page_id%20from%20page_admin%20where%20uid="+str(response['id'])+"&access_token="+response['access_token']
        print urlopen(url).read()