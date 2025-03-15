from rest_framework import serializers
from .models import Payer, PayerGroup, PayerDetails

class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = '__all__'
