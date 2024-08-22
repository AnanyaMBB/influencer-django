# urls.py
from django.urls import path
from .views import ExecutePaymentView, PayoutView, CreatePaymentView
from . import views

urlpatterns = [
    path('api/create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('api/execute-payment/', ExecutePaymentView.as_view(), name='execute-payment'),
    path('api/payout/', PayoutView.as_view(), name='payout'),
    path('api/wallet/get', views.getWallet, name='getWallet'),
    path('api/transactions/get', views.getTransactions, name='getTransactions'),
]
