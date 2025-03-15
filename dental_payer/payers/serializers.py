from rest_framework import serializers
from .models import Payer, PayerDetail

class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = '__all__'

class PayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayerDetail
        fields = '__all__'
