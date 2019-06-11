from django.urls import path

from . import views

app_name='tracker'
urlpatterns = [
    path('', views.index, name='index'),
    path('block/<int:height>/', views.blockTracker, name='blockTracker'),    
    path('address/list/', views.addressList, name='addressList'),
    path('address/list/<int:page>', views.addressListPage, name='addressListPage'),
    path('address/<str:address>', views.address, name='addressInfo'),
    path('addressTx/<str:address>/', views.addressTx, name='addressTx'),
    path('addressTx/<str:address>/<int:page>', views.addressTxPage, name='addressTxPage'),
    path('contract/list/', views.contractsList, name='contractsList'),
    path('contract/list/<int:page>', views.contractsListPage, name='contractsListPage'),
    path('contract/<str:address>', views.contract, name='contractInfo'),
    path('contractTx/<str:address>/', views.contractTx, name='contractTx'),
    path('contractTx/<str:address>/<int:page>', views.contractTxPage, name='contractTxPage'),
    path('block/list/', views.blockList, name='blockList'),
    path('block/list/<int:page>', views.blockListPage, name='blockListPage'),
    path('blockTx/<int:height>/', views.blockTx, name='blockTx'),
    path('blockTx/<int:height>/<int:page>', views.blockTxPage, name='blockTxPage'),
    path('transaction/list/', views.txList, name='txList'),
    path('transaction/list/<int:page>', views.txListPage, name='txListPage'),
    path('transaction/<str:txHash>/', views.transactionTracker, name='txTracker'),
    path('token/list/',views.tokenList, name='tokenList'),
    path('token/list/<int:page>',views.tokenListPage, name='tokenListPage'),
    path('token/transfers/', views.tokenTransfers, name='tokenTransfers'),
    path('token/transfers/<int:page>', views.tokenTransfersPage, name='tokenTransfersPage'),
    path('token/<str:address>', views.token, name='tokenInfo'),
    path('tokentx/<str:address>/', views.tokenTx, name='tokenTx'),
    path('tokentx/<str:address>/<int:page>', views.tokenTxPage, name='tokenTxPage'),
    path('search/', views.search, name='search'),
]
