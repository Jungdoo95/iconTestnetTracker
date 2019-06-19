from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

import geoip2.database
import os
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

