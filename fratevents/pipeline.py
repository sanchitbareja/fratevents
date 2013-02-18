from social_auth.backends.facebook import FacebookBackend
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
from urllib2 import urlopen
from userprofile.models import UserProfile
import time, datetime
from fratevents.settings import AWS_UPLOAD_DESTINATION

def create_user_profile(backend, details, response, social_user, uid, user, *args, **kwargs):
    # create user profile here.
    if len(UserProfile.objects.filter(user = user)) == 0:
        new_user_birthday = time.strptime(response['birthday'].replace("/"," "),"%d %m %Y")
        new_user = UserProfile(user = user, birthday = datetime.date(year=new_user_birthday.tm_year,month=new_user_birthday.tm_mon,day=new_user_birthday.tm_mday))
        new_user.save()

def get_user_profile_pic(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    print response
    print backend
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/%s/picture?type=large" % response['id']
 
    if url:
        profile_pic = urlopen(url).read()
        fout = open(response['id'], "wb") #filepath is where to save the image
        fout.write(profile_pic)
        fout.close()
        default_storage.save(str(response['id'])+'.jpg',File(open(response['id'],'rwb')))
        #save profile pic to user profile
        user = UserProfile.objects.get(user = user)
        user.profilePic = AWS_UPLOAD_DESTINATION+str(response['id'])+".jpg"
        user.save()

def get_user_events(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/"+str(response['id'])+"/events?access_token="+str(response['access_token'])
        # print urlopen(url).read()

def get_user_network(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/fql?q=select%20affiliations%20from%20user%20where%20uid="+str(response['id'])+"&access_token="+response['access_token']
        # print urlopen(url).read()

def get_user_pages(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "https://graph.facebook.com/fql?q=select%20page_id%20from%20page_admin%20where%20uid="+str(response['id'])+"&access_token="+response['access_token']
        # print urlopen(url).read()