from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Device
from django.utils import timezone

class DeviceIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        device_id = request.META.get('HTTP_DEVICEID')
        if not device_id:
            raise AuthenticationFailed('Device ID is required')

        try:
            device = Device.objects.get(deviceID=device_id)
            
        except Device.DoesNotExist:
            # Device ID not found, create a new device
            device = Device.objects.create(deviceID=device_id)
        device.last_login = timezone.now()  # Update last_login on authentication
        device.save()
        return (device, None)
