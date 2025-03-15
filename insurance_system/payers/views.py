from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Payer
from .serializers import PayerSerializer

class PayerViewSet(viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer
