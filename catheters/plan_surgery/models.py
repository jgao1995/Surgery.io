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
    # product_type = models.CharField(max_length=200)

    notes = models.TextField()
    useful_links = models.CharField() # JSON

    dimensions = JSONField()

    def __str__(self):
        return '{1} - {0}, {3} \n {2}'.format(self.manufacturer, self.brand_name, self.description, self.product_type)


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






#### GRAPH DATABASE ####

class DeviceType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fields = models.CharField() # JSON LIST of STRINGS
    def __str__(self):
        return name

class TypeDependency(models.Model):
    # DeviceType 1 [foreign key], DeviceType 2 [foreign key], field1[str], field2[str], comparator[str]
    device_type_1 = models.ForeignKey(DeviceType)
    device_type_2 = models.ForeignKey(DeviceType)
    field_1 = models.CharField(max_length=200)
    field_2 = models.CharField(max_length=200)
    comparator = models.CharField(max_length=2)



def create_device_type(name, fields):
    field_str = json.dumps(fields)
    device_type = DeviceType(name=name, fields=field_str)
    return device_type

def createDummyDependency():
    wire = create_device_type('Wire', ['thickness', 'length'])
    catheter = create_device_type('Catheter', ['max_outer_diameter', 'min_inner_diameter', 'length'])
    wire.save()
    catheter.save()
    # new dependency between wire and catheter
    dependency = TypeDependency(device_type_1=wire, device_type_2=catheter, field_1='thickness', field_2='min_inner_diameter', comparator='>')


def createDependency(type_1, type_2, field_1, field_2, comparator):
    for arg in [field_1, field_2, comparator]:
        if not isinstance(arg, str):
            raise Exception('Argument is not a string: %s'%arg)
    if comparator not in ['<', '<=', '>', '>=', '=']:
        raise Exception("Comparator must be in ['<', '<=', '>', '>=', '=']")
    # make sure those fields are in the device types
    fields_1 = json.loads(type_1.fields) # should be a [str]
    fields_2 = json.loads(type_2.fields) # should be a [str]
    if field_1 not in fields_1:
        raise Exception("%s not in %s's fields:"%(field_1, type_1.name))
    fields_2 = json.loads(type_2.fields) # should be a [str]
    if field_2 not in fields_2:
        raise Exception("%s not in %s's fields:"%(field_2, type_2.name))
    # We're good. create the dependency

    dependency = TypeDependency(device_type_1=type_1, device_type_2=type_2, field_1=field_1, field_2=field_2, comparator=comparator)
    dependency.save()
    
    return dependency











