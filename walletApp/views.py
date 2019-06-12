from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic
import json

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


# Create your views here.


def index(request):
    return render(request, 'wallet/index.html')


def createWallet(request):    
    wallet = KeyWallet.create()
    print("address : ", wallet.get_address())
    print("private key : ", wallet.get_private_key())
    wallet_json = { "address" : wallet.get_address(),
                    "private_key" : wallet.get_private_key()}
    return JsonResponse(wallet_json);

def searchWallet(request):
    print(str(request.body))
    data = json.loads(request.body)    
    j = json.loads(data)
    print(j['private_key'])    
    wallet = KeyWallet.load(str.encode(j['private_key']))
    params = { "address" : wallet.get_address()}    
    res = requests.get("https://bicon.tracker.solidwallet.io/v3/address/info", params=params)
    walletData = res.json()

    return JsonResponse(walletData.get('data'))
