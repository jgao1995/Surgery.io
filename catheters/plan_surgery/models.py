from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from jsonfield import JSONField

import json

# Create your models here.

class Device(models.Model):
    manufacturer = models.CharField(max_length=500)
    brand_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)

    dimensions = JSONField()

    def __str__(self):
        return '{}|{}|{}|{}'.format(self.manufacturer, self.brand_name, self.description, self.product_type)


class Surgery(models.Model):
    devices = models.ManyToManyField(Device)
    created_date = models.DateTimeField(default=timezone.now)

def add_device_to_database(manufacturer, brand_name, description, product_type, dims=None):
    ''' take in all that stuff ^
    return true/false if it works out'''
    dimensions = dims or {}
    device = Device(manufacturer=manufacturer, brand_name=brand_name, description=description, dimensions=json.dumps(dimensions))

    device.save()

def create_surgery():
    surgery = Surgery()
    surgery.save()
    return surgery

def add_device_to_surgery(device):
    # Assume device has been saved.
    surgery.devices.add(device)
    return device


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)