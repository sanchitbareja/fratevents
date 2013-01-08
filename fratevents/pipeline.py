from social_auth.backends.facebook import FacebookBackend
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File

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
        default_storage.save(str(response['id']),File(open(response['id'],'rwb')))
    

def get_user_events(backend, details, response, social_user, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/%s/events?access_token=%s" % response['id'],response['access_token']