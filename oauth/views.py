from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Users
from django.utils import timezone

import requests, json
import uuid

# Create your views here.

def index(request):
    if 'login' in request.session:
        if request.session['login']:
            check = login(request)
            if check == "email":
                return HttpResponseRedirect("/oauth/input/email/")
            else:
                del request.session['code']
    if request.GET:
        return render(request, 'oauth/index.html', dict(request.GET))
    return render(request, 'oauth/index.html')

def login(request):
    if 'kakao' in request.session:
        loginType = 'kakao'
        email = request.session['kakao']
    elif 'facebook' in request.session:
        loginType = 'facebook'
        email = request.session['facebook']
    elif 'google' in request.session:
        loginType = 'google'
        email = request.session['google']
    
    print(email)
    if email == "require_userEmail":
        try:
            user = Users.objects.get(code= request.session['code'], loginType=loginType)
            user.lastAccess = timezone.now()            
            request.session[loginType] = user.email
            user.save()
        except:
            print("Email input page...")
            return "email"        
    else:
        try:
            user = Users.objects.get(email= email, code= request.session['code'],loginType=loginType)
            user.lastAccess = timezone.now()
            user.save()
        except:
            user = Users(email=email, code= request.session['code'],loginType=loginType)
            user.save()

    

def inputEmail(request):
    if 'login' not in request.session:         
        return HttpResponseRedirect('/oauth/?msg='+'please login first!'+'&status=Warning')

    if request.method == 'GET':
        if request.session['login']:
            return render(request, 'oauth/inputEmail.html')
        else:
            return HttpResponseRedirect('/oauth/?msg='+'please login first!'+'&status=Warning')
    else :
        if 'kakao' in request.session:
            request.session['kakao']  = request.POST['email']
        elif 'facebook' in request.session:
            request.session['facebook'] = request.POST['email']
        elif 'google' in request.session:
            request.session['google'] = request.POST['email']

        return HttpResponseRedirect('/oauth/')
        

def logout(request):
    print("logout...")
    del request.session['login']
    if 'kakao' in request.session:
        print("kakao logout...")
        headers={
            "Authorization": "Bearer "+request.session['kakaoToken']
        }
        requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
        del request.session['kakao']
        del request.session['kakaoToken']
        print("success!")
    elif 'facebook' in request.session:
        print("facebook logout...")
        del request.session['facebook']
        del request.session['facebookToken']
    elif 'google' in request.session:
        print("google logout...")
        del request.session['google']
        del request.session['googleToken']
    
    print("Logout successful! redirect login page...")
    return HttpResponseRedirect('/oauth/')

def kakaoLogin(request):
    params={
        "client_id":"ce9e623119a6eaf17429360798694f13",
        "redirect_uri":"http://localhost:8000/oauth/kakao/response",
        "response_type":"code"
    }
    
    return HttpResponseRedirect("https://kauth.kakao.com/oauth/authorize?client_id=ce9e623119a6eaf17429360798694f13&redirect_uri=http://localhost:8000/oauth/kakao/response&response_type=code");

def kakaoLoginResponse(request):
    queryString = dict(request.GET)
    for key, value in queryString.items():
            print("key > " + key+ "\nvalue > "+str(value))
    try:
        if queryString['code']:
            params={
                "grant_type": "authorization_code",
                "client_id": "ce9e623119a6eaf17429360798694f13",
                "redirect_uri":"http://localhost:8000/oauth/kakao/response",
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
                return HttpResponseRedirect("https://kauth.kakao.com/oauth/authorize?"+
                                    "client_id=ce9e623119a6eaf17429360798694f13"+
                                    "&redirect_uri=http://localhost:8000/oauth/kakao/response"+
                                    "&response_type=code"+
                                    '&scope=account_email');
            elif email=="require_userEmail":                
                pass
            else:            
                request.session['kakao'] = email
                request.session['kakaoToken']=token['access_token']
            request.session['login'] = True
            return HttpResponseRedirect('/oauth/')
        else:
            return HttpResponseRedirect('/oauth/?msg='+'kakao login fail'+'&status=fail')
    except:
        return HttpResponseRedirect('/oauth/?msg='+'kakao login fail'+'&status=fail')
        
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
    request.session['code'] = res.json()['id']
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
        "redirect_uri":"http://localhost:8000/oauth/kakao/response",
        "state":{
            "user" : request.session['facebook_state'],
            "st" : request.session.session_key
        }
    }
    print(params)
    return HttpResponseRedirect("https://www.facebook.com/v3.3/dialog/oauth?"+
                                "client_id=394590811398500"+
                                '&redirect_uri=http://localhost:8000/oauth/facebook/response'+
                                '&state="{"user":'+request.session['facebook_state']+',"st":'+request.session.session_key+'}"');

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
    request.session['facebookToken'] = token
    email = facebookGetEmail(request,token)
    if email=="fail":
        request.session['facebook'] = "require_userEmail"
    else:
        request.session['facebook'] = email
    request.session['login'] = True

    return HttpResponseRedirect("/oauth/"); 

def facebookGetToken(code):
    url = "https://graph.facebook.com/v3.3/oauth/access_token"
    params ={
        "client_id": "394590811398500",
        "redirect_uri": "http://localhost:8000/oauth/facebook/response",
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
    request.session['code'] = res.json()['id']
    if 'email' in res.json():
        return res.json()['email']
    else:
        return "fail"

def googleLogin(request):
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    params={
        "client_id": "750220603857-thg1p249rsuitirhgo5seurmg4ak5ufe.apps.googleusercontent.com",
        "redirect_uri" : "http://localhost:8000/oauth/google/response",
        "scope" : "https://www.googleapis.com/auth/userinfo.email"
    }
    # googleLoginUri = 
    return HttpResponseRedirect(url+"?"
                                    +"client_id="+params['client_id']
                                    +"&redirect_uri="+params['redirect_uri']
                                    +"&scope="+params['scope']
                                    +"&response_type=code")

def googleLoginResponse(request):
    print(request.GET.dict())
    if 'code' not in request.GET.dict():
        return HttpResponseRedirect("/oauth/google/login")
    else:
        authCode = request.GET.dict()['code']
        data = {
            'code' : authCode,
            "client_id" : "750220603857-thg1p249rsuitirhgo5seurmg4ak5ufe.apps.googleusercontent.com",
            "client_secret" : "KxZJovH51EN6Aa-eZXtDjCb8",
            "redirect_uri" : "http://localhost:8000/oauth/google/response",
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
            return HttpResponseRedirect("/oauth/google/login")
        else:
            request.session['googleToken'] = tokens['access_token']
            email = googleGetEmail(request,tokens['access_token'])
            if email != "fail":
                request.session['google'] = email
            else:
                request.session['google'] = "require_userEmail"

            request.session['login'] = True
            return HttpResponseRedirect("/oauth/")
            


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
    request.session['code'] = emailJson['sub']
    print(emailJson)
    if "email" in emailJson:
        return emailJson['email']
    else:
        return "fail"