'''
facebook Oauth 처리부
'''

from .common import *

def facebookLogin(request):
    request.session['facebook_state'] = uuid.uuid4().hex[:8].upper()
    if not request.session.session_key:
        request.session.save()
    params={
        "client_id":"394590811398500",
        "redirect_uri":"http://localhost:8000/user/login/facebook/response",
        "state":{
            "user" : request.session['facebook_state'],
            "st" : request.session.session_key
        }
    }
    url = "https://www.facebook.com/v3.3/dialog/oauth"
    print(params)
    return HttpResponseRedirect(createRedirectURL(url, params));

def facebookLoginResponse(request):
    print(request.GET)
    print(type(request.GET))
    print(dict(request.GET))
    
    params = (request.GET.dict())
    print(params)
    
    if 'user' in params['state']:
        user = params['state']
        print(user)

    if 'code' in params:
        print("code : "+params['code'])
    
    token = facebookGetToken(params['code'])
    request.session['loginToken'] = "facebook."+token
    email = facebookGetEmail(request,token)
    if email=="fail":
        request.session['email'] = "require_userEmail"
    else:
        request.session['email'] = email
    request.session['login'] = True

    return HttpResponseRedirect("/user/login/"); 

def facebookGetToken(code):
    url = "https://graph.facebook.com/v3.3/oauth/access_token"
    params ={
        "client_id": "394590811398500",
        "redirect_uri": "http://localhost:8000/user/login/facebook/response",
        "client_secret": "aa1a8f1598eebc955653901a9983cb9a",
        "code": code
    }
    print(params)
    res = requests.get(url, params=params)
    print(res.json())
    return res.json()['access_token']

def facebookGetEmail(request,token):
    url = "https://graph.facebook.com/me"

    params={
        "fields" : "email",
        "access_token" : token
    }
    res = requests.get(url, params=params)
    print("facebook email ...")
    print(res.json())
    print(res.json()['id'])
    # request.session['code'] = res.json()['id']
    if 'email' in res.json():
        return res.json()['email']
    else:
        return "fail"