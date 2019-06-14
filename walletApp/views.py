from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic

import requests
import math
from bs4 import BeautifulSoup
import json
import shutil
import os
import glob

from django.views.decorators.csrf import csrf_exempt

#iconsdk
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet
#endiconsdk
# Creates an IconService instance using the HTTP provider and set a provider.
icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io/api/v3", 3))

BASE_DIR = os.path.dirname(os.path.abspath(__file__));
# Create your views here.


def index(request):
    # request.session['wallet_name'] = 'default';
    return render(request, 'wallet/index.html')


def createWallet(request):
    print(request.body)
    postData = json.loads(request.body)
    data = json.loads(postData)
    wallet = KeyWallet.create()
    wallet_status = { "status" : "ok"}
    print( os.path.dirname(os.path.abspath(__file__)))
    os.mkdir(BASE_DIR+"/keystore/"+request.session.session_key+'/')
    wallet.store( BASE_DIR+"/keystore/"+request.session.session_key+'/'+data['wallet_name'],data['wallet_password'])
    request.session['wallet_name'] = data['wallet_name']
    request.session['wallet_password'] = data['wallet_password']
    # file_path = BASE_DIR+wallet.get_address()+"/keystore"
    # wallet.store(file_path,"keystore")
    return JsonResponse(wallet_status);

def keystoreDownload(request): 
    file_path= BASE_DIR+"/keystore/"+request.session.session_key+'/'+request.session['wallet_name']
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def walletPrivateKey(request):
    try:
        file_path= BASE_DIR+"/keystore/"+request.session.session_key+'/'+request.session['wallet_name']
        wallet = KeyWallet.load(file_path, request.session['wallet_password'])
        wallet_json = { "address" : wallet.get_address(),
                        "private_key" : wallet.get_private_key()}
        return JsonResponse(wallet_json)
    except Exception:
        return JsonResponse({"ERROR": 404})

def walletCreateClose(request):
    result = {"status": "ok"}
    try:
        file_path= BASE_DIR+"/keystore/"+request.session.session_key
        if os.path.exists(file_path):
            shutil.rmtree(file_path, ignore_errors=True)
    except Exception:
        print("NOT FOUND FILE PATH")        
        result['status'] = "fail"
    finally:
        try:
            del request.session['wallet_name']
            del request.session['wallet_password']    
        except:
            result['status']="fail"
    return JsonResponse(result)
    

def searchWallet(request):    
    # print(request.body);
    if os.path.exists (BASE_DIR+"/keystore/"+request.session.session_key+'/'+request.session['keystore']):
        try:
            data = json.loads(request.body)
            j = json.loads(data)
            password = j['keystore_password']
            wallet = KeyWallet.load(BASE_DIR+"/keystore/"+request.session.session_key+'/'+request.session['keystore'],password);
            params = { "address" : wallet.get_address()}
            print("wallet addr >> "+ wallet.get_address())        
            return JsonResponse(params)
        except Exception as e:
            return JsonResponse({"status":"fail", "msg":str(e)})

    try:
        data = json.loads(request.body)    
        # print("json.loads(value) >> "+data)
        # print(type(data))  
        j = json.loads(data)
        # print("json.loads(json) >> "+j['private_key'])
        key = bytes.fromhex(j['private_key'])
        # print("bytes json['private_key'] >> ")
        # print(key)
        wallet = KeyWallet.load(key)
        params = { "address" : wallet.get_address()}
        print("wallet addr >> "+ wallet.get_address())        
        return JsonResponse(params)
    except Exception:
        return JsonResponse({"status":"fail"})


def uploadKeystore(request):
    if request.method == 'POST':        
        if 'keystore' in request.FILES:
            
            keystore = request.FILES['keystore']
            keystore_name = keystore._name
            print(os.path.exists(BASE_DIR+"/keystore/"+request.session.session_key+'/'))
            if not os.path.exists (BASE_DIR+"/keystore/"+request.session.session_key+'/'):
                print("folder create!!!")
                os.mkdir(BASE_DIR+"/keystore/"+request.session.session_key+'/')
            fp = open(BASE_DIR+'/keystore/'+request.session.session_key+'/'+keystore_name, 'wb')
            for chunk in keystore.chunks():
                fp.write(chunk)
            fp.close()
            request.session['keystore'] = keystore_name;
            return HttpResponse('ok')
        else:
            print('no keystore detective')
            print(request.FILES);
    else:
        print('no post')
    return HttpResponse('fail')
    
