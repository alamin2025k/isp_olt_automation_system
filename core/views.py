# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import OLTDevice, MikroTikDevice, ONU
from .forms import OLTDeviceForm, MikroTikDeviceForm # Create these forms
# from .tasks import fetch_onu_status, remove_onu_from_olt # Celery tasks

@login_required
def dashboard_view(request):
    total_olts = OLTDevice.objects.count()
    total_mikrotiks = MikroTikDevice.objects.count()
    total_onus = ONU.objects.count()
    online_onus = ONU.objects.filter(is_online=True).count()
    offline_onus = ONU.objects.filter(is_online=False).count()
    return render(request, 'dashboard.html', {
        'total_olts': total_olts,
        'total_mikrotiks': total_mikrotiks,
        'total_onus': total_onus,
        'online_onus': online_onus,
        'offline_onus': offline_onus,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser) # Only superusers can add devices
def add_olt_device(request):
    if request.method == 'POST':
        form = OLTDeviceForm(request.POST)
        if form.is_valid():
            # In a real scenario, you'd test connection here before saving
            form.save()
            messages.success(request, "OLT Device added successfully!")
            return redirect('olt_list') # Redirect to OLT list page
        else:
            messages.error(request, "Error adding OLT device.")
    else:
        form = OLTDeviceForm()
    return render(request, 'add_device.html', {'form': form, 'device_type': 'OLT'})

# Similar views for add_mikrotik_device, olt_list, mikrotik_list, etc.

@login_required
def onu_status_search(request):
    onu = None
    if request.method == 'GET' and 'username' in request.GET:
        username = request.GET.get('username')
        try:
            onu = ONU.objects.get(customer_username=username)
            # You might trigger a real-time fetch here using Celery if status is critical
            # fetch_onu_status.delay(onu.id)
            messages.info(request, "Displaying current ONU status.")
        except ONU.DoesNotExist:
            messages.warning(request, "ONU for this username not found.")
    return render(request, 'onu_status.html', {'onu': onu})

@login_required
def offline_onu_list(request):
    offline_onus = ONU.objects.filter(is_online=False).order_by('offline_since')
    return render(request, 'offline_onu_list.html', {'offline_onus': offline_onus})

@login_required
@user_passes_test(lambda u: u.is_superuser) # Only superusers can remove ONUs
def remove_offline_onu(request, onu_id):
    if request.method == 'POST':
        onu = get_object_or_404(ONU, id=onu_id, is_online=False)
        try:
            # Trigger Celery task to remove from OLT
            # remove_onu_from_olt.delay(onu.id)
            # For now, just mark as removed in DB
            onu.delete() # Or set a status like is_removed=True
            messages.success(request, f"ONU {onu.sn} successfully removed.")
        except Exception as e:
            messages.error(request, f"Error removing ONU {onu.sn}: {e}")
        return redirect('offline_onu_list')
    # If not POST, just redirect back or show a confirmation page
    return redirect('offline_onu_list')
