# urls.py
from django.urls import path
from .views import CreatePaymentView, ExecutePaymentView

urlpatterns = [
    path('api/create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('api/execute-payment/', ExecutePaymentView.as_view(), name='execute-payment'),
]
