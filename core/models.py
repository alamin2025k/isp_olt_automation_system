# core/models.py
from django.db import models

class OLTDevice(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255) # Store hashed/encrypted password!
    brand = models.CharField(max_length=50, choices=[
        ('huawei', 'Huawei'),
        ('zte', 'ZTE'),
        ('fiberhome', 'FiberHome'),
        ('cdata', 'C-Data'),
        ('other', 'Other')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class MikroTikDevice(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255) # Store hashed/encrypted password!
    api_port = models.IntegerField(default=8728)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class ONU(models.Model):
    olt = models.ForeignKey(OLTDevice, on_delete=models.CASCADE, related_name='onus')
    sn = models.CharField(max_length=50, unique=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    customer_username = models.CharField(max_length=100, blank=True, null=True) # Link to MikroTik user
    olt_port = models.CharField(max_length=50)
    is_online = models.BooleanField(default=False)
    last_seen_online = models.DateTimeField(null=True, blank=True)
    offline_since = models.DateTimeField(null=True, blank=True)
    rx_power = models.FloatField(null=True, blank=True) # Optical power received
    tx_power = models.FloatField(null=True, blank=True) # Optical power transmitted
    # Add other relevant ONU details as needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ONU {self.sn} on {self.olt.name}"

    @property
    def offline_duration(self):
        if not self.is_online and self.offline_since:
            from django.utils import timezone
            duration = timezone.now() - self.offline_since
            # Format duration nicely (e.g., "2h 30m")
            return str(duration).split('.')[0] # Basic formatting
        return None
