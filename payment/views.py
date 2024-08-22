# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
# from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
# from django.conf import settings

# # Set up PayPal client
# environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
# client = PayPalHttpClient(environment)

# class CreatePaymentView(APIView):
#     def post(self, request):
#         create_order = OrdersCreateRequest()
#         create_order.prefer('return=representation')
#         create_order.request_body({
#             "intent": "CAPTURE",
#             "purchase_units": [{
#                 "amount": {
#                     "currency_code": "USD",
#                     "value": "5.00"
#                 }
#             }]
#         })

#         try:
#             response = client.execute(create_order)
#             return Response({"id": response.result.id}, status=status.HTTP_201_CREATED)
#         except IOError as ioe:
#             return Response({"error": str(ioe)}, status=status.HTTP_400_BAD_REQUEST)

# class ExecutePaymentView(APIView):
#     def post(self, request):
#         order_id = request.data.get('orderID')
#         capture_order = OrdersCaptureRequest(order_id)

#         try:
#             response = client.execute(capture_order)
#             return Response({
#                 "status": response.result.status,
#                 "id": response.result.id
#             })
#         except IOError as ioe:
#             return Response({"error": str(ioe)}, status=status.HTTP_400_BAD_REQUEST)

import requests
from requests.auth import HTTPBasicAuth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from decimal import Decimal
from django.conf import settings
from .models import Wallet, Transaction
from . import serializers
import time
import base64

# Set up PayPal client for the Checkout SDK
environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
client = PayPalHttpClient(environment)

def get_paypal_access_token():
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'  # Use api.paypal.com for live environment
    auth_header = base64.b64encode(f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_CLIENT_SECRET}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {'grant_type': 'client_credentials'}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("GETTING ACCESS TOKEN")
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.text}")

class CreatePaymentView(APIView):
    def post(self, request): 
        amount = request.data.get('amount')
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        create_order = OrdersCreateRequest()
        create_order.prefer('return=representation')
        create_order.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": amount  # Use the amount passed from the frontend
                }
            }]
        })

        try:
            response = client.execute(create_order)
            return Response({"id": response.result.id}, status=status.HTTP_201_CREATED)
        except IOError as ioe:
            return Response({"error": str(ioe)}, status=status.HTTP_400_BAD_REQUEST)
        

class ExecutePaymentView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('orderID')
        capture_order = OrdersCaptureRequest(order_id)

        try:
            response = client.execute(capture_order)
            if response.result.status == 'COMPLETED':
                
                # Update wallet balance
                
                userObject = User.objects.get(username=request.data.get('username'))
                wallet, created = Wallet.objects.get_or_create(user=userObject)
                capture = response.result.purchase_units[0].payments.captures[0]
                amount = Decimal(capture.amount.value)  # Convert to Decimal
                wallet.balance += amount
                wallet.save()

                # Log the transaction
                Transaction.objects.create(
                    user=userObject,
                    transaction_type='topup',
                    amount=amount,
                    status='COMPLETED',
                    paypal_order_id=order_id
                )

                return Response({
                    "status": response.result.status,
                    "id": response.result.id
                })
            else:
                return Response({"status": "FAILED"}, status=status.HTTP_400_BAD_REQUEST)

        except IOError as ioe:
            return Response({"error": str(ioe)}, status=status.HTTP_400_BAD_REQUEST)

class PayoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(username=request.data.get('username'))    
        wallet = Wallet.objects.get(user=user)
        amount = Decimal(request.data.get('amount'))

        if amount > wallet.balance:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        # Get PayPal access token
        try:
            access_token = get_paypal_access_token()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create the payout request
        url = 'https://api.sandbox.paypal.com/v1/payments/payouts'  # Use api.paypal.com for live environment
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payout_data = {
            "sender_batch_header": {
                "sender_batch_id": f"payout_{user.id}_{int(time.time())}",
                "email_subject": "You have a payout!"
            },
            "items": [{
                "recipient_type": "EMAIL",
                "amount": {
                    "value": str(amount),
                    "currency": "USD"
                },
                "receiver": user.email,
                "note": "Thanks for your service!",
                "sender_item_id": f"item_{user.id}_{int(time.time())}"
            }]
        }

        response = requests.post(url, headers=headers, json=payout_data)

        if response.status_code == 201:  # HTTP 201 Created
            response_data = response.json()

            # Deduct the amount from the wallet balance
            wallet.balance -= amount
            wallet.save()

            # Log the transaction
            Transaction.objects.create(
                user=user,
                transaction_type='payout',
                amount=amount,
                status='SUCCESS',
                paypal_order_id=response_data['batch_header']['payout_batch_id']
            )

            return Response({"status": "PAYOUT_SUCCESSFUL"})
        else:
            return Response({"error": response.json()}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getWallet(request):
    user = User.objects.get(username=request.GET.get("username"))
    wallet = Wallet.objects.get(user=user)
    return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getTransactions(request): 
    user = User.objects.get(username=request.GET.get("username"))
    transactions = Transaction.objects.filter(user=user)
    serializer = serializers.TransacionsSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
