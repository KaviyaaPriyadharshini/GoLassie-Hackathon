from django.db import models

class PayerGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Payer(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(PayerGroup, on_delete=models.CASCADE)

class PayerDetails(models.Model):
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    payer_number = models.CharField(max_length=50, null=True, blank=True)
    tax_id = models.CharField(max_length=50, null=True, blank=True)
    raw_name = models.CharField(max_length=255)
