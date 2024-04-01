from .models import Device, Account, Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import DeviceIDAuthentication
from django.utils import timezone

class TestLogin(APIView):
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
        try:
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

class deleteCard(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def delete(self, request):
        data = request.data

        try:
            number = data.get("card_number")
            cards = Account.objects.get(cardNumber=number)
            cards.delete()
            
            return Response({'message': "Deleted the card"})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class setLimit(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def put(self, request):
        data = request.data

        try:
            number = data.get("card_number")
            card = Account.objects.get(cardNumber=number)
            card.limits = data.get("limits")
            card.save()
            return Response({'message': "Updated successfully"})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class addTransaction(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def post(self, request):
        data = request.data
        print(data)
        try:
            device = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            card = Account.objects.get(cardNumber = request.data.get('card_number'))
            time = timezone.now()
            transaction_info = {
                'device': device,
                'card': card,
                'credit_debit': request.data.get('credit_debit'),
                'amount': request.data.get('amount'),
                'category': request.data.get('category'),
                'timestamp': time
            }
            transaction = Transaction.objects.create(**transaction_info)
            return Response({
                'message': 'Transaction created successfully',
                'transaction': data
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getTransactions(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transactions = Transaction.objects.filter(device = deviceID)
            transaction_data = []
            for t in transactions:
                transaction_data.append({
                    'id': t.id,
                    'credit_debit': t.credit_debit,
                    'amount': t.amount,
                    'category': t.category,
                    'timestamp': t.timestamp
                })
            return Response({
                'transactions': transaction_data
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class deleteTransaction(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def delete(self, request):
        data = request.data
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transaction = Transaction.objects.get(id = data.get('id'))
            transaction.delete()
            return Response({
                'message': "Successfully deleted transaction"
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class updateTransaction(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def put(self, request):
        data = request.data
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transaction = Transaction.objects.get(id = data.get('id'))
            transaction.limits = data.get("amount")
            transaction.save()
            return Response({
                'message': "Successfully updated"
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)
