from django.db import models

class Device(models.Model):
    deviceID = models.CharField(max_length=255, primary_key=True)
    last_login = models.DateTimeField(auto_now=True)

class Account(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    nickname = models.TextField()
    holderName = models.TextField()
    cardType = models.TextField()
    cardProvider = models.TextField()
    bankName = models.TextField()
    validity = models.TextField()
    cardNumber = models.TextField(primary_key=True)
    CVV = models.TextField()
    limits = models.IntegerField()

class Transaction(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    card = models.ForeignKey(Account, on_delete=models.CASCADE)
    credit_debit = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Limits(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    card = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    total_earnt = models.DecimalField(max_digits=10, decimal_places=2)
    percent_used = models.IntegerField()