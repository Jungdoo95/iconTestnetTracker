from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic
import json
import shutil
import os

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
    request.session['wallet_name'] = 'default';
    return render(request, 'wallet/index.html')


def createWallet(request):
    print(request.body)
    postData = json.loads(request.body)
    data = json.loads(postData)
    wallet = KeyWallet.create()
    print("address : ", wallet.get_address())
    print("private key : ", wallet.get_private_key())
    wallet_status = { "status" : "ok"}
    print( os.path.dirname(os.path.abspath(__file__)))
    wallet.store( BASE_DIR+"/keystore/"+data['wallet_name'],data['wallet_password'])
    request.session['wallet_name'] = data['wallet_name']
    request.session['wallet_password'] = data['wallet_password']
    # file_path = BASE_DIR+wallet.get_address()+"/keystore"
    # wallet.store(file_path,"keystore")
    return JsonResponse(wallet_status);

def keystoreDownload(request): 
    file_path= BASE_DIR+"/keystore/"+request.session['wallet_name']
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def walletPrivateKey(request):
    try:
        file_path= BASE_DIR+"/keystore/"+request.session['wallet_name']
        wallet = KeyWallet.load(file_path, request.session['wallet_password'])
        wallet_json = { "address" : wallet.get_address(),
                        "private_key" : wallet.get_private_key()}
        return JsonResponse(wallet_json)
    except Exception:
        return JsonResponse({"ERROR": 404})

def walletCreateClose(request):
    result = {"status": "ok"}
    try:
        file_path= BASE_DIR+"/keystore/"+request.session['wallet_name']
        if os.path.exists(file_path):
            os.remove(file_path)
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
    print(request.body);
    data = json.loads(request.body)    
    print(data)
    print(type(data))  
    j = json.loads(data)
    print(j['private_key'])
    key = bytes(j['private_key'],'utf8')
    print(key)
    wallet = KeyWallet.load(key)
    params = { "address" : wallet.get_address()}    
    res = requests.get("https://bicon.tracker.solidwallet.io/v3/address/info", params=params)
    walletData = res.json()

    return JsonResponse(walletData.get('data'))
