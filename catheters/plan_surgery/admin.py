from django.contrib import admin

# Register your models here.

from .models import Device, DeviceType, TypeDependency, Surgery, DeviceDependency

admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(TypeDependency)
admin.site.register(Surgery)
admin.site.register(DeviceDependency)