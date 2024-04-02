from .models import Device, Account, Transaction, Limit
from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import DeviceIDAuthentication
from django.utils import timezone

#General
class TestLogin(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        device = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
        # Only authenticated requests will reach here
        return Response({"last_login":device.last_login})

class deleteUserData(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def delete(self, request):
        try:
            device = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            if request.data.get("api_key") == "101928383":
                device.delete()
                return Response({
                    "message": "Deleted"
                })
            else:
                return Response({
                    "message": "wrong api key"
                })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

# Cards
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
            limit = Limit.objects.create(device=device, card=account)
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

            return Response(
                    card_data
                )
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
            limit, created = Limit.objects.get_or_create(device = card.device, card = card)
            card.limits = data.get("limits")
            card.save()
            limit.percent_used = ((limit.total_spent-limit.total_earnt)/data.get("limits"))*100
            limit.save()
            return Response({'message': "Updated successfully"})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

# Transactions
class addTransaction(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def post(self, request):
        data = request.data
        try:
            device = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            card = Account.objects.get(cardNumber = request.data.get('card_number'))
            limits, created = Limit.objects.get_or_create(device=device, card=card)
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
            if request.data.get('credit_debit') == "credit":
                limits.total_earnt += request.data.get('amount')
            else:
                limits.total_spent += request.data.get('amount')
            limits.percent_used = ((limits.total_spent-limits.total_earnt)/card.limits)*100
            limits.save()
            return Response({
                'message': 'Transaction created successfully',
                'transaction': data,
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
                    'card': t.card.nickname,
                    'credit_debit': t.credit_debit,
                    'amount': t.amount,
                    'category': t.category,
                    'timestamp': t.timestamp
                })
            return Response(
                transaction_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class deleteTransaction(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def delete(self, request):
        data = request.data
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transaction = Transaction.objects.get(id = data.get('id'))
            card = transaction.card
            #limit = Limit.objects.get_or_create(device=deviceID, card=card)
            transaction_amount = transaction.amount
            #limit.total_spent -= transaction.amount
            #limit.percent_used = (limit.total_spent/card.limits)*100
            #limit.save()
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
            card = transaction.card
            limit, created = Limit.objects.get_or_create(device = deviceID, card = card)
            amount_changed = data.get("amount")-transaction.amount
            if transaction.credit_debit == "credit":
                limit.total_earnt += amount_changed
            else:
                limit.total_spent += amount_changed
            limit.percent_used = ((limit.total_spent-limit.total_earnt)/card.limits)*100
            transaction.amount = data.get("amount")
            limit.save()
            transaction.save()
            return Response({
                'message': "Successfully updated"
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getDebitTransactions(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transactions = Transaction.objects.filter(device = deviceID, credit_debit="debit")
            transaction_data = []
            for t in transactions:
                transaction_data.append({
                    'id': t.id,
                    'card': t.card.nickname,
                    'credit_debit': t.credit_debit,
                    'amount': t.amount,
                    'category': t.category,
                    'timestamp': t.timestamp
                })
            return Response(
                transaction_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getCreditTransactions(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transactions = Transaction.objects.filter(device = deviceID, credit_debit="credit")
            transaction_data = []
            for t in transactions:
                transaction_data.append({
                    'id': t.id,
                    'credit_debit': t.credit_debit,
                    'amount': t.amount,
                    'category': t.category,
                    'timestamp': t.timestamp
                })
            return Response(
                transaction_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getCategoryTransactions(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transactions = Transaction.objects.filter(device = deviceID, category = request.data.get("category"))
            transaction_data = []
            for t in transactions:
                transaction_data.append({
                    'id': t.id,
                    'credit_debit': t.credit_debit,
                    'amount': t.amount,
                    'category': t.category,
                    'timestamp': t.timestamp
                })
            return Response(
                transaction_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getCardTransactions(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transactions = Transaction.objects.filter(device = deviceID, card = request.data.get("cardNumber"))
            transaction_data = []
            for t in transactions:
                transaction_data.append({
                    'id': t.id,
                    'credit_debit': t.credit_debit,
                    'amount': t.amount,
                    'category': t.category,
                    'timestamp': t.timestamp
                })
            return Response(
                transaction_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getCardCategoryTransactions(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            transactions = Transaction.objects.filter(device = deviceID, category = request.data.get("category"), card = request.data.get("cardNumber"))
            transaction_data = []
            for t in transactions:
                transaction_data.append({
                    'id': t.id,
                    'credit_debit': t.credit_debit,
                    'amount': t.amount,
                    'category': t.category,
                    'timestamp': t.timestamp
                })
            return Response(
               transaction_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

# Limits
class getLimits(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            limits = Limit.objects.filter(device = deviceID)
            limit_data = []
            for t in limits:
                t.percent_used = t.percent_used if t.percent_used<100 else 100
                limit_data.append({
                    'card': t.card.nickname,
                    'total_spent': t.total_spent,
                    'total_earnt': t.total_earnt,
                    'percent_used': t.percent_used,
                    'fractional_percent': t.percent_used/100 if t.percent_used>0 else 0
                })
            return Response(
                limit_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getTotalLimits(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            limits = Limit.objects.filter(device = deviceID)
            limit_data = []
            expense = 0
            total_limit = 0
            for t in limits:
                expense += t.total_spent-t.total_earnt 
                total_limit += t.card.limits
            total_limit = total_limit if expense > 0 else total_limit-expense
            expense = expense if expense>0 else 0
            percentage = round((expense/total_limit)*100)
            return Response({
                'expense': expense, 
                'limit': total_limit,
                'percentage': percentage
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class getLimitsCard(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            card = Account.objects.get(card_number = request.data.get('card_number'))
            limits = Limit.objects.filter(device = deviceID)
            limit_data = []
            for t in limits:
                limit_data.append({
                    'card': t.card.cardNumber,
                    'total_spent': t.total_spent,
                    'total_earnt': t.total_earnt,
                    'percent_used': t.percent_used
                })
            return Response(
                limit_data
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)     

class resetLimit(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def delete(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            limits = Limit.objects.filter(device = deviceID)
            for limit in limits:
                limit.delete()
                limit.save()
            return Response({"message": "Deleted"})
        except Exception as e:
            return Response({'error': str(e)}, status=400) 

class getCreditDebit(APIView):
    authentication_classes = [DeviceIDAuthentication]

    def get(self, request):
        try:
            deviceID = Device.objects.get(deviceID = request.META.get('HTTP_DEVICEID'))
            print(request)
            creditTransactions = Transaction.objects.filter(device = deviceID, credit_debit="credit")
            debitTransactions = Transaction.objects.filter(device = deviceID, credit_debit="debit")
            credit = 0
            debit = 0
            for creditT in creditTransactions:
                credit += creditT.amount
            for debitT in debitTransactions:
                debit += debitT.amount
    
            return Response({
                "incoming": credit,
                "expense": debit
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400) 