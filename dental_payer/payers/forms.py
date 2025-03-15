from django import forms
from .models import PayerDetail, UploadedFile,Payer, PayerGroup

class PayerDetailForm(forms.ModelForm):
    class Meta:
        model = PayerDetail
        fields = ['payer', 'payer_number', 'tax_id', 'source']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class UnmapPayerForm(forms.Form):
    payer_group = forms.ModelChoiceField(queryset=PayerGroup.objects.all())
    payer = forms.ModelChoiceField(queryset=Payer.objects.all())