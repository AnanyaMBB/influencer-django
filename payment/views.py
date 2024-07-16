from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from django.conf import settings

# Set up PayPal client
environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
client = PayPalHttpClient(environment)

class CreatePaymentView(APIView):
    def post(self, request):
        create_order = OrdersCreateRequest()
        create_order.prefer('return=representation')
        create_order.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": "5.00"
                }
            }]
        })

        try:
            response = client.execute(create_order)
            return Response({"id": response.result.id}, status=status.HTTP_201_CREATED)
        except IOError as ioe:
            return Response({"error": str(ioe)}, status=status.HTTP_400_BAD_REQUEST)

class ExecutePaymentView(APIView):
    def post(self, request):
        order_id = request.data.get('orderID')
        capture_order = OrdersCaptureRequest(order_id)

        try:
            response = client.execute(capture_order)
            return Response({
                "status": response.result.status,
                "id": response.result.id
            })
        except IOError as ioe:
            return Response({"error": str(ioe)}, status=status.HTTP_400_BAD_REQUEST)