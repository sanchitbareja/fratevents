from social_auth.backends.facebook import FacebookBackend

def get_user_profile_pic(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    print response
    print backend
    if backend.__class__ == FacebookBackend:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
 
    if url:
        print "url"
        print url