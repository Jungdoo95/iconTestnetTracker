from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import geoip2.database
import os
import requests
import ast
import json
from ipware.ip import get_ip

BASE_DIR = os.path.dirname(os.path.abspath(__file__));
geo = geoip2.database.Reader(BASE_DIR+"/data/city/GeoLite2-City.mmdb")

# Create your views here.
def index(request):
    ip = get_ip(request)
    # ip = "211.60.153.215"
    if ip is not None:
        print(ip)
        try:
            ipLocation = geo.city(ip)
            latitude = ipLocation.location.latitude
            longitude = ipLocation.location.longitude
            print("ip location!")
            return render(request, 'geolocation/index.html', {"status": "ok","latitude":latitude,"longitude":longitude})
        except:
            pass

    return render(request, 'geolocation/index.html')

@csrf_exempt
def insertArea(request):
    if request.method == "GET":
        return render(request, 'geolocation/insertArea.html')
    else:
        print(dict(request.POST))
        pathData = dict(request.POST)['area0'][0]
        print(pathData)
        print(type(pathData))
        path = ast.literal_eval(pathData);
        print(path)
        print(type(path))
        return render(request, 'geolocation/editInfo.html', {"path": pathData})

@csrf_exempt
def locationSearch(request):
    # key ce9e623119a6eaf17429360798694f13
    # url https://dapi.kakao.com/v2/local/geo/coord2regioncode.json
    x = request.POST['x']
    y = request.POST['y']
    print({"x":x,"y":y})
    headers={
        "Authorization": "KakaoAK "+"ce9e623119a6eaf17429360798694f13"
    }
    res = requests.get('https://dapi.kakao.com/v2/local/geo/coord2address.json', headers=headers,params={"x":x,"y":y})
    print(res.json())
    return HttpResponse(res.text, content_type="application/json")
