from django.shortcuts import render

from rest_framework import generics
from .models import Device, Account, Transaction
from .serializers import DeviceSerializer, AccountSerializer, TransactionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .authentication import DeviceIDAuthentication
from .models import Account, Device, Transaction


class DeviceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    authentication_classes = [DeviceIDAuthentication]  # Add authentication

class AccountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [DeviceIDAuthentication]  # Add authentication

class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [DeviceIDAuthentication]  # Add authentication

class MyAuthenticatedAPIView(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        device = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
        # Only authenticated requests will reach here
        return Response({"last_login":device.last_login})

class addAccount(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def post(self, request):
        data = request.data
        device = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
        card_info = {
            'device': device,
            'nickname': data.get('nickname'),
            'holderName': data.get('holder_name'),
            'cardType': data.get('card_type'),
            'cardProvider': data.get('card_provider'),
            'bankName': data.get('bank_name'),
            'validity': data.get('validity'),
            'cardNumber': data.get('card_number'),
            'CVV': data.get('cvv'),
            'limits': data.get('limits')
        }
        try:
            account = Account.objects.create(**card_info)
            return Response({
                'message': 'Account created successfully',
                'card': data
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getCards(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        data = request.data
        

        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            cards = Account.objects.filter(device=deviceID)

            card_data = []
            for card in cards:
                card_data.append({
                    'nickname': card.nickname,
                    'holderName': card.holderName,
                    'cardType': card.cardType,
                    'cardProvider': card.cardProvider,
                    'bankName': card.bankName,
                    'validity': card.validity,
                    'cardNumber': card.cardNumber,
                    'CVV': card.CVV,
                    'limits': card.limits
                })

            return Response({'cards': card_data})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
