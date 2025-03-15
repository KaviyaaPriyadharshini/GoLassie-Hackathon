from django.contrib import admin

# Register your models here.
from .models import PayerGroup, Payer, PayerDetails
#Password=askckpd@04

class PayerDetailsInline(admin.TabularInline):  
    model = PayerDetails
    extra = 1 

@admin.register(PayerGroup)
class PayerGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    list_filter = ('group',)
    search_fields = ('name',)
    inlines = [PayerDetailsInline]  

@admin.register(PayerDetails)
class PayerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'raw_name', 'payer', 'payer_number', 'tax_id')
    list_filter = ('payer',)
    search_fields = ('raw_name', 'payer_number', 'tax_id')
