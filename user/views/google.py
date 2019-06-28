'''
google Oauth 처리부
'''

from .common import *

def googleLogin(request):
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    params={
        "client_id": "750220603857-thg1p249rsuitirhgo5seurmg4ak5ufe.apps.googleusercontent.com",
        "redirect_uri" : "http://localhost:8000/user/login/google/response",
        "scope" : "https://www.googleapis.com/auth/userinfo.email",
        "response_type":"code"
    }
    # googleLoginUri = 
    return HttpResponseRedirect( createRedirectURL(url, params))

def googleLoginResponse(request):
    print(request.GET.dict())
    if 'code' not in request.GET.dict():
        return HttpResponseRedirect("/user/login/google/")
    else:
        authCode = request.GET.dict()['code']
        data = {
            'code' : authCode,
            "client_id" : "750220603857-thg1p249rsuitirhgo5seurmg4ak5ufe.apps.googleusercontent.com",
            "client_secret" : "KxZJovH51EN6Aa-eZXtDjCb8",
            "redirect_uri" : "http://localhost:8000/user/login/google/response",
            "grant_type" : "authorization_code",
            "scope" : "https://www.googleapis.com/auth/userinfo.email"
        }
        res = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
        
        print(res.json()['expires_in'])
        print(res.json()['access_token'])
        tokens = res.json()
        for key, value in tokens.items():
            # print("key >> "+key)
            print (key+" >> %10s" % value)
        if tokens['expires_in'] <= 0:
            return HttpResponseRedirect("/user/login/google/")
        else:
            request.session['loginToken'] = "google."+tokens['access_token']
            email = googleGetEmail(request,tokens['access_token'])
            if email != "fail":
                request.session['email'] = email
            else:
                request.session['email'] = "require_userEmail"

            request.session['login'] = True
            return HttpResponseRedirect("/user/login/")
            


def googleGetEmail(request,token):
    headers={
        "Authorization": "Bearer "+token
    }
    params={        
        "access_token" : token,
        "field" : "email"  
    }
    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    res = requests.get(url, headers=headers, params=params)
    emailJson = res.json()
    print(emailJson['sub'])
    # request.session['code'] = emailJson['sub']
    print(emailJson)
    if "email" in emailJson:
        return emailJson['email']
    else:
        return "fail"