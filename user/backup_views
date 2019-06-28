from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from .models import User
from .forms import *
from django.utils import timezone

import requests, json
import re
import uuid

def createRedirectURL(url, params):
    redirectURL = url;
    if not params:
        return redirectURL;
    else :
        redirectURL+="?"
        for key , value in params.items():
            if isinstance( value ,str):
                redirectURL += key+"="+value+"&"
            else:
                redirectURL += key+"="+json.dumps(value)+"&"
                
        redirectURL = redirectURL[:-1]
        print(redirectURL)
        return redirectURL;

# Create your views here.
def index(request):
    if 'login' in request.session:
        if request.session['login']:
            check = loginCheck(request)
            if check == "email":
                return HttpResponseRedirect("/user/require/email/")
            elif check == "fail":
                try:
                    del request.session['login']
                    del request.session['loginToken']
                except:
                    return render(request, 'user/login.html')                
            else:
                return render(request, 'user/login.html')
    if request.GET:
        return render(request, 'user/login.html', dict(request.GET))
    return render(request, 'user/login.html')

def login(request):    
    if 'login' in request.session:
        if request.session['login']:
            check = loginCheck(request)
            if check == "email":
                return HttpResponseRedirect("/user/require/email/")
            elif check == "fail":
                try:
                    del request.session['login']
                    del request.session['loginToken']
                except:
                    return render(request, 'user/login.html')     
            elif check =="profile":
                return HttpResponseRedirect("/user/require/profile/")           
            else:
                return render(request, 'user/login.html')   
    if request.GET:
        return render(request, 'user/login.html', dict(request.GET))
    return render(request, 'user/login.html')

def loginCheck(request):
    if 'email' in request.session:
        email = request.session['email']
    else:
        return "fail"
    
    if 'loginToken' not in request.session:
        return "fail"

    if email == "require_userEmail":
        return "email"        
    else:
        try:
            user = User.objects.get(email= email)
            user.lastAccess = timezone.now()
            user.save()
        except:
            user = User(email=email)
            user.save()
        if not user.name or not user.phoneNumber:
            print("require Profile!")    
        if not user.walletAddress:
            print("require walletAddress!")
            return "profile"

    

def inputEmail(request):
    if 'login' not in request.session:         
        return HttpResponseRedirect('/user/login/?msg='+'please login first!'+'&status=Warning')

    if request.method == 'GET':
        if request.session['login']:
            return render(request, 'user/inputEmail.html')
        else:
            return HttpResponseRedirect('/user/login/?msg='+'please login first!'+'&status=Warning')
    else :
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            return HttpResponseRedirect('/user/require/email')
        except:
            if 'email' in request.session:
                request.session['email']  = email

        return HttpResponseRedirect('/user/login/')

def inputProfile(request):
    if request.method =='GET':        
        
        return render(request, 'user/modify/profile.html')        
    else:
        print(request.POST)
        form = UserProfileForm(request.POST)
        if  form.is_valid():
            print("test msg")
            user = User.objects.get(email = request.session['email'])
            user.name = request.POST['name']
            user.phoneNumber = request.POST['phoneNumber']
            user.walletAddress = request.POST['walletAddress']
            user.save()
        return HttpResponseRedirect('/user/login/')

def logout(request):
    print("logout...")
    del request.session['login']
    if 'kakao' in request.session['loginToken']:
        print("kakao logout...")
        headers={
            "Authorization": "Bearer "+re.sub('(kakao).',"",request.session['loginToken'])
        }
        requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
        del request.session['email']
        del request.session['loginToken']
        print("success!")
    else :
        print("facebook logout...")
        del request.session['email']
        del request.session['loginToken']
    
    print("Logout successful! redirect login page...")
    return HttpResponseRedirect('/user/login/')

def kakaoLogin(request):
    url = "https://kauth.kakao.com/oauth/authorize"
    params={
        "client_id":"ce9e623119a6eaf17429360798694f13",
        "redirect_uri":"http://localhost:8000/user/login/kakao/response",
        "response_type":"code"
    }
    kakaoOauthUrl = createRedirectURL(url, params)
    return HttpResponseRedirect(kakaoOauthUrl);

def kakaoLoginResponse(request):
    queryString = dict(request.GET)

    try:
        if queryString['code']:
            params={
                "grant_type": "authorization_code",
                "client_id": "ce9e623119a6eaf17429360798694f13",
                "redirect_uri":"http://localhost:8000/user/login/kakao/response",
                "code": queryString['code'],
            }
            headers={
                "Content-type":"application/x-www-form-urlencoded;charset=utf-8"
            }

            res = requests.post("https://kauth.kakao.com/oauth/token", headers=headers, params=params)
            token = res.json()
            print(token)
            email = kakaoEmailRequest(request, token['access_token'])
            print("Email >> "+email)
            if email == "require_kakao_accoutEmail":
                print("kakao Email Request!")
                url = "https://kauth.kakao.com/oauth/authorize"
                params={
                    "client_id":"ce9e623119a6eaf17429360798694f13",
                    "redirect_uri":"http://localhost:8000/user/login/kakao/response",
                    "response_type":"code",
                    "scope":"account_email"
                }
                return HttpResponseRedirect(createRedirectURL(url, params));
            elif email=="require_userEmail":                
                pass
            else:            
                request.session['email'] = email
                request.session['loginToken']="kakao."+token['access_token']
            request.session['login'] = True
            return HttpResponseRedirect('/user/login')
        else:
            return HttpResponseRedirect('/user/login/?msg='+'kakao login fail'+'&status=fail')
    except:
        return HttpResponseRedirect('/user/login/?msg='+'kakao login fail'+'&status=fail')
        
def kakaoEmailRequest(request, token):
    params='property_keys=["kakao_account.email"]'
    headers={
        "Authorization": "Bearer "+token,
        "Content-type" : "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers, data=params)
    print(res)
    print("Profile test >> ")    
    print(res.json())
    print(res.json()['id'])
    # request.session['code'] = res.json()['id']
    try:
        print("email check...")
        print(res.json()['kakao_account']['email'])
        if res.json()['kakao_account']['email']:
            print("kakao email true..")
            return res.json()['kakao_account']['email']
    except:
        print("email not found...")
        try:
            print("email require true...?")
            if res.json()['kakao_account']['email_needs_agreement']:
                return "require_kakao_accoutEmail"
        except:
            print("user email require...")
            return "require_userEmail"
        
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