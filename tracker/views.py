from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import requests
import math
from bs4 import BeautifulSoup

TEST_NET="https://bicon.tracker.solidwallet.io/v3"
# Create your views here.
def index(request):
    res = requests.get(TEST_NET+"/main/mainInfo")
    mainData = res.json()
    res = requests.get(TEST_NET+"/main/mainChart")
    mainChart = res.json()
    return render(request, 'tracker/index.html',{"mainData":mainData,"mainChart":mainChart})

def blockTracker(request, height):
    params = {"height":height}
    res = requests.get(TEST_NET+"/block/info",params=params)
    blockInfo = res.json()    
    params['page'] = request.GET.get('page','1')
    params['count'] = request.GET.get('count','10')
    res = requests.get(TEST_NET+"/block/txList",params=params)
    blockTx = res.json()
    return render(request, 'tracker/block/block.html', {"blockInfo":blockInfo.get('data'),"blockTx":blockTx.get('data')})

def blockTx(request, height):
    params = {"height":height}
    params['page'] = request.GET.get('page','1')
    params['count'] = request.GET.get('count','10')
    res = requests.get(TEST_NET+"/block/txList",params=params)
    blockTx = res.json()
    maxPage = int(blockTx.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/block/blockTxList.html', {"blockTx":blockTx.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "height":height})

def blockTxPage(request, height):
    params = {"height":height}
    params['page'] = request.GET.get('page','1')
    params['count'] = request.GET.get('count','10')
    res = requests.get(TEST_NET+"/block/txList",params=params)
    blockTx = res.json()
    maxPage = int(blockTx.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/block/blockTxList.html', {"blockTx":blockTx.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "height":height})

def transactionTracker(request, txHash):
    params = {"txHash":txHash}
    res = requests.get(TEST_NET+"/transaction/txDetail",params=params)
    tx = res.json()
    params['page'] = request.GET.get('page','1')
    params['count'] = request.GET.get('count','10')
    res = requests.get(TEST_NET+"/transaction/internalTxList",params=params)
    internalTx = res.json()
    return render(request, 'tracker/transaction/txDetail.html',{"transaction":tx.get('data'),"internalTx":internalTx.get('data')})

def addressList(request):
    params = { "page": request.GET.get('page','1'), "count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/address/list", params=params)
    addressList = res.json()
    maxPage = int(addressList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/address/addressList.html', {"addressList":addressList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})
def addressListPage(request, page):
    params = { "page": page, "count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/address/list", params=params)
    addressList = res.json()
    maxPage = int(addressList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/address/addressList.html', {"addressList":addressList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def address(request, address):
    params = {"address":address}
    res = requests.get(TEST_NET+"/address/info", params=params)
    addressInfo = res.json()
    tokens = addressInfo.get('data').get('tokenList')
    totalUSD= 0
    for token in tokens:
        if token.get('totalTokenPrice') != None:
            totalUSD += token.get('totalTokenPrice')
    
    params['page']=request.GET.get('page','1')
    params['count']=request.GET.get('count','10')
    res = requests.get(TEST_NET+"/address/txList", params=params)
    addressTxList = res.json()
    return render(request, "tracker/address/address.html", {"addressInfo":addressInfo.get('data'),"totalUSD": totalUSD,"addressTxList":addressTxList.get('data')})

def addressTx(request, address):
    params = {"address":address}
    params['page']=1
    params['count']=request.GET.get('count','10')
    res = requests.get(TEST_NET+"/address/txList", params=params)
    addressTx = res.json()
    maxPage = int(addressTx.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/address/addressTxList.html', {"addressTxList":addressTx.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "address":address})

def addressTxPage(request, address, page):
    params = {"address":address}
    params['page']=page
    params['count']=request.GET.get('count','10')
    res = requests.get(TEST_NET+"/address/txList", params=params)
    addressTx = res.json()
    maxPage = int(addressTx.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/address/addressTxList.html', {"addressTxList":addressTx.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "address":address})

def contractsList(request):
    params = {"page":request.GET.get('page','1'),"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/contract/list", params=params)
    contractsList = res.json()
    maxPage = int(contractsList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/address/contractsList.html', {"contractsList":contractsList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def contractsListPage(request,page):
    params = {"page":page,"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/contract/list", params=params)
    contractsList = res.json()
    maxPage = int(contractsList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/address/contractsList.html', {"contractsList":contractsList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def contract(request, address):
    params={"addr":address}
    res = requests.get(TEST_NET+"/contract/info", params=params)
    contractInfo = res.json()
    params['page']=request.GET.get('page','1')
    params['count']=request.GET.get('count','10')
    res = requests.get(TEST_NET+"/contract/txList", params=params)
    contractTxList = res.json()
    return render(request, "tracker/address/contract.html", {"contractInfo":contractInfo.get('data'),"contractTxList":contractTxList.get('data')})

def contractTx(request, address):
    params={"addr":address}
    params['page']=request.GET.get('page','1')
    params['count']=request.GET.get('count','25')
    res = requests.get(TEST_NET+"/contract/txList", params=params)
    contractTxList = res.json()
    maxPage = int(contractTxList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, "tracker/address/contractTxList.html", {"contractTxList":contractTxList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "address":address})

def contractTxPage(request, address, page):
    params={"addr":address}
    params['page']=page
    params['count']=request.GET.get('count','25')
    res = requests.get(TEST_NET+"/contract/txList", params=params)
    contractTxList = res.json()
    maxPage = int(contractTxList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, "tracker/address/contractTxList.html", {"contractTxList":contractTxList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "address":address})

def blockList(request):
    params={"page":request.GET.get('page','1'),"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/block/list", params=params)
    blockList = res.json()
    maxPage = int(blockList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/block/blockList.html', {"blockList":blockList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def blockListPage(request, page):
    params={"page":page,"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/block/list", params=params)
    blockList = res.json()
    maxPage = int(blockList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/block/blockList.html', {"blockList":blockList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def txList(request):
    params={"page":request.GET.get('page','1'),"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/transaction/recentTx", params=params)
    txList = res.json()
    maxPage = int(txList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/transaction/txList.html', {"txList":txList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def txListPage(request, page):
    params={"page":page,"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/transaction/recentTx", params=params)
    txList = res.json()
    maxPage = int(txList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/transaction/txList.html', {"txList":txList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def token(request, address):
    params={"contractAddr":address}
    res = requests.get(TEST_NET+"/token/summary", params=params)
    tokenInfo = res.json()
    params['page'] = request.GET.get('page','1')
    params['count'] = request.GET.get('count','10')
    res = requests.get(TEST_NET+"/token/txList", params=params)
    tokenTx = res.json()
    return render(request,'tracker/token/token.html', {"tokenInfo":tokenInfo.get('data'),"tokenTx":tokenTx.get('data')})

def tokenTx(request, address):
    params={"contractAddr":address}   
    params['page'] = request.GET.get('page','1')
    params['count'] = request.GET.get('count','10')
    res = requests.get(TEST_NET+"/token/txList", params=params)
    tokenTx = res.json()
    maxPage = int(tokenTx.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request,'tracker/token/tokenTxList.html', {"tokenTx":tokenTx.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "address":address})

def tokenTxPage(request, address, page):
    params={"contractAddr":address}   
    params['page'] = page
    params['count'] = request.GET.get('count','10')
    res = requests.get(TEST_NET+"/token/txList", params=params)
    tokenTx = res.json()
    maxPage = int(tokenTx.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request,'tracker/token/tokenTxList.html', {"tokenTx":tokenTx.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"], "address":address})

def tokenList(request):
    params={"page":request.GET.get('page','1'),"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/token/list", params=params)
    tokenList = res.json()
    maxPage = int(tokenList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/token/tokenList.html', {"tokenList":tokenList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})


def tokenListPage(request,page):
    params={"page":page,"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/token/list", params=params)
    tokenList = res.json()
    maxPage = int(tokenList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/token/tokenList.html', {"tokenList":tokenList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})


def tokenTransfers(request):
    params={"page":request.GET.get('page','1'),"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/token/txList", params=params)
    tokenTransfersList = res.json()
    maxPage = int(tokenTransfersList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/token/tokenTransfers.html', {"tokenTransfersList":tokenTransfersList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})

def tokenTransfersPage(request, page):
    params={"page":page,"count":request.GET.get('count','25')}
    res = requests.get(TEST_NET+"/token/txList", params=params)
    tokenTransfersList = res.json()
    maxPage = int(tokenTransfersList.get('listSize')) / int(params["count"])
    maxPage = math.ceil(maxPage)
    return render(request, 'tracker/token/tokenTransfers.html', {"tokenTransfersList":tokenTransfersList.get('data'),"page":params["page"],"maxPage":maxPage,"count":params["count"]})


def search(request):
    keyword = None
    if request.method == "POST":
        keyword = request.POST['keyword']
    

    if keyword.find('0x') == 0:
        params={"hash":keyword}
        res = requests.get(TEST_NET+"/block/info",params=params)
        blockInfo = res.json()
        if( blockInfo.get('result') == '200'):
            height = blockInfo.get('data').get('height')
            return HttpResponseRedirect( reverse('tracker:blockTracker', args=(height,) ) )
        else:
            return render(request, 'tracker/error/no_search_keyword.html')
    elif keyword.find('cx') == 0:
        return HttpResponseRedirect(reverse('tracker:contractInfo', args=(keyword,) ) )
    elif keyword.find('hx') ==0:
        return HttpResponseRedirect(reverse('tracker:addressInfo', args=(keyword,) ) )
    else :
        return render(request, 'tracker/error/no_search_keyword.html')