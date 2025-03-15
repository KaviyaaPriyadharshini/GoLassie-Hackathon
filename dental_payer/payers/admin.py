from django.contrib import admin
from .models import Payer, PayerDetail, PayerGroup

admin.site.register(PayerGroup)
admin.site.register(Payer)
admin.site.register(PayerDetail)
