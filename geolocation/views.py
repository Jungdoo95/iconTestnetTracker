from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import *

import geoip2.database
import os
import requests
import ast
import json
import string
import random
import base64
from ipware.ip import get_ip

BASE_DIR = os.path.dirname(os.path.abspath(__file__));
geo = geoip2.database.Reader(BASE_DIR+"/data/city/GeoLite2-City.mmdb")

def randomString(stringLength=20):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
# Create your views here.
def index(request):
    allArea = area.objects.values().all()
    print(type(allArea))
    # print(allArea.dict())
    print(allArea[0])
    print(type(allArea[0]))
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

    return render(request, 'geolocation/index.html', {"areas": list(allArea)})

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
def editInfo(request):
    if request.method == "POST":
        print(request.POST);
        myDict = request.POST.dict()
        # data = json.loads(request.POST);
        print(myDict);
        print("\n");
        for key , value in myDict.items():
            if( len(value)> 30):
                print(key+" >> "+ value[:30]+"...")
            else:
                print (key +" >> "+value)
        print("\n");
        if "base64" in myDict['img']:
            src = myDict['img']
            imgType = src[src.find('/')+1:src.find(';')]
            src = src[src.find(',')+1:]
            while True:
                imgName = randomString()+"."+imgType
                imgPath = BASE_DIR+"/static/images/maps/"+imgName; 
                if os.path.exists(imgPath): continue
                break
            img = open(imgPath, 'wb')
            img.write(base64.b64decode(src))
            img.close()
            myDict['img']= "/static/images/maps/"+imgName;
        try:
            data = area(title=myDict['titleName'],
                        titleBG=myDict['titleBGColor'],
                        titleColor = myDict['titleColor'],
                        ellipsis = myDict['ellipsis'],
                        jibun = myDict['jibun'],
                        path = myDict['path'],
                        img_src = myDict['img'],
                        link = myDict['link']
                        )
            data.save()
            return HttpResponse(json.dumps({'message': "success"}), content_type='application/json')
        except:
            print("editInfo fail!")
            response = HttpResponse(json.dumps({'message': "fail to upload"}), 
            content_type='application/json')
            response.status_code = 400
            return response

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
