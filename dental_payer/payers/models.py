from django.db import models

class PayerGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

def get_default_payer_group():
    group, _ = PayerGroup.objects.get_or_create(name="Default Group")
    return group.id

class Payer(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(
        PayerGroup, 
        on_delete=models.CASCADE, 
        related_name='payers',
        default=get_default_payer_group 
    )
    pretty_name = models.CharField(max_length=255, blank=True, null=True)
    is_mapped = models.BooleanField(default=True)

class PayerDetail(models.Model):
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, related_name='details')
    payer_number = models.CharField(max_length=50, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.payer.name} ({self.payer_number if self.payer_number else 'No Payer Number'})"


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
