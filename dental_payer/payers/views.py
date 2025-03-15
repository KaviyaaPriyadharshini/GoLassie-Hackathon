from rest_framework import viewsets
from .models import Payer, PayerDetail, PayerGroup
from .serializers import PayerSerializer, PayerDetailSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PayerDetailForm, UploadFileForm,UnmapPayerForm
from django.contrib import messages
from .utils import process_uploaded_file

class PayerViewSet(viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer

class PayerDetailViewSet(viewsets.ModelViewSet):
    queryset = PayerDetail.objects.all()
    serializer_class = PayerDetailSerializer


def manage_payer_groups(request):
    """ View to display and add new payer groups """
    if request.method == "POST":
        name = request.POST.get("name").strip()
        if name:
            PayerGroup.objects.create(name=name)
            messages.success(request, f"Payer Group '{name}' added successfully!")
            return redirect("manage_payer_groups")  
    
    payer_groups = PayerGroup.objects.all()
    return render(request, "manage_payer_groups.html", {"payer_groups": payer_groups})


def edit_payer_group(request, group_id):
    """ View to edit a payer group name """
    payer_group = get_object_or_404(PayerGroup, id=group_id)

    if request.method == "POST":
        new_name = request.POST.get("name").strip()
        if new_name:
            payer_group.name = new_name
            payer_group.save()
            messages.success(request, f"Payer Group '{new_name}' updated successfully!")
            return redirect("manage_payer_groups")

    return render(request, "edit_payer_group.html", {"payer_group": payer_group})


def delete_payer_group(request, group_id):
    """ View to delete a payer group """
    payer_group = get_object_or_404(PayerGroup, id=group_id)
    
    if request.method == "POST":
        payer_group.delete()
        messages.success(request, f"Payer Group '{payer_group.name}' deleted successfully!")
        return redirect("manage_payer_groups")

    return render(request, "confirm_delete.html", {"payer_group": payer_group})
def dashboard(request):
    payers = Payer.objects.all()  
    payer_groups = PayerGroup.objects.all()  
    payer_details = PayerDetail.objects.all()  

    context = {
        'payers': payers,
        'payer_groups_count': payer_groups.count(),
        'payers_count': payers.count(),
        'payer_details_count': payer_details.count()
    }
    return render(request, 'index.html', context)

def manual_mapping(request):
    if request.method == "POST":
        form = PayerDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manual_mapping')
    else:
        form = PayerDetailForm()

    return render(request, 'manual_mapping.html', {'form': form})


def upload_payer_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()
            message = process_uploaded_file(file_instance.file)
            messages.success(request, message)
            return redirect('upload_payer_file')
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

def payer_hierarchy(request):
    """ View to display the payer hierarchy """
    payer_groups = PayerGroup.objects.prefetch_related("payers").all()  
    return render(request, "payer_hierarchy.html", {"payer_groups": payer_groups})

def edit_payer(request, payer_id):
    """ View to edit a payer """
    payer = get_object_or_404(Payer, id=payer_id)

    if request.method == "POST":
        new_name = request.POST.get("name").strip()
        pretty_name = request.POST.get("pretty_name").strip()

        if new_name:
            payer.name = new_name
            payer.pretty_name = pretty_name
            payer.save()
            messages.success(request, f"Payer '{new_name}' updated successfully!")
            return redirect("dashboard")

    return render(request, "edit_payer.html", {"payer": payer})

def delete_payer(request, payer_id):
    """ View to delete a payer """
    payer = get_object_or_404(Payer, id=payer_id)

    if request.method == "POST":
        payer_name = payer.name
        payer.delete()
        messages.success(request, f"Payer '{payer_name}' deleted successfully!")
        return redirect("dashboard")

    return render(request, "confirm_delete_payer.html", {"payer": payer})
def unmap_payer(request):
    if request.method == 'POST':
        payer_ids = request.POST.getlist('payer_ids')
        for payer_id in payer_ids:
            payer = Payer.objects.get(id=payer_id)
            payer.is_mapped = False
            payer.save()
        messages.success(request, 'Payers unmapped successfully')
        return redirect('payer_hierarchy')
    return render(request, 'unmap_payer.html')

def unmapped_payers(request):
    unmapped_payers = Payer.objects.filter(is_mapped=False)
    return render(request, 'unmapped_payers.html', {'unmapped_payers': unmapped_payers})