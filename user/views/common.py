'''
views 공용 라이브러리나 함수

createRedirectURL 
    - Oauth 특성상 타 사이트 이동하여 처리하는 경우가 많아 생성
    - 파라미터 값으로 문자열 형식의 url 과 dictionary 형식의 params으로 받음
    - 결과 값으로는 url?params_key=value....과 같음
'''

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from ..models import User
from ..forms import *
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

def loginCheckDeco(func):
    def decolate(*arg,  **kwargs):
        if loginCheck(*arg,  **kwargs):            
            return func(*arg,  **kwargs)
        else:
            return HttpResponseRedirect("/user/login/")
    return decolate

def loginCheck(request):
    url = request.build_absolute_uri()
    print("REQUEST URL - "+url)
    print("REQUIRE LOGIN ")
    if request.session['login']:
        print("LOGIN CHECK      [OK]")
        print(f"LOGIN EMAIL      [{request.session['email']}]")
        return True;
    return False;