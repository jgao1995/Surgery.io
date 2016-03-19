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
    product_type = models.ForeignKey(DeviceType)

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

class DeviceDependency(models.Model): 
    # device 1, device 2
    device_1 = models.ForeignKey(Device)
    device_2 = models.ForeignKey(Device)
    edgeType = models.IntegerField()

    def __str__(self): 
        return '{0} to {1} has dependecy {2}'.format(self.device_1, self.device_2, self.edgeType)

def createDependencies():
    devices = Device.objects.all()
    # for each device, look at the relationship with every other device
    for device in devices: 
        for other in devices: 
            # look in the rules graph for the right rule
            rules = TypeDependency.filter(device_type_1 = device.product_type, device_type_2 = other.product_type)
            if(len(rules) != 1):
                print "Invalid Rule Graph"
            # get the rule out 
            rule = rules[0]
            # parse the fields to compare out of each 
            params_1 = json.loads((getattr(device, 'dimensions')))[rule.field_1]
            params_2 = json.loads((getattr(other, 'dimensions')))[rule.field_2]
            edge = 0
            if(rule.comparator == '<'):
                if(params_1 < params_2):
                    edge = 1
                else:
                    edge = 0

            if(rule.comparator == '>'):
                if(params_1 > params_2):
                    edge = 1
                else:
                    edge = 0

            if(rule.comparator == '='):
                if(params_1 == params_2):
                    edge = 1
                else:
                    edge = 0

            if(rule.comparator == '<='):
                if(params_1 <= params_2):
                    edge = 1
                else:
                    edge = 0

            if(rule.comparator == '>='):
                if(params_1 >= params_2):
                    edge = 1
                else:
                    edge = 0
            dependence = DeviceDependency(device_1 = device, device_2 = other, edgeType = edge)
            dependence.save()
    return


def updateDependencies():
    devices = Device.objects.all()
    # for each device, look at the relationship with every other device
    for device in devices: 
        for other in devices: 
            # look in the rules graph for the right rule
            rules = TypeDependency.filter(device_type_1 = device.product_type, device_type_2 = other.product_type)
            device_relationship = DeviceDependency.filter(device_1 = device, device_2 = other)[0]
            if(len(rules) != 1):
                print "Invalid Rule Graph"
            # get the rule out 
            rule = rules[0]
            # parse the fields to compare out of each 
            params_1 = json.loads((getattr(device, 'dimensions')))[rule.field_1]
            params_2 = json.loads((getattr(other, 'dimensions')))[rule.field_2]

            if(rule.comparator == '<'):
                if(params_1 < params_2):
                    device_relationship.edgeType = 1
                else:
                    device_relationship.edgeType = 0
                device_relationship.save()

            if(rule.comparator == '>'):
                if(params_1 > params_2):
                    device_relationship.edgeType = 1
                else:
                    device_relationship.edgeType = 0
                device_relationship.save()

            if(rule.comparator == '='):
                if(params_1 == params_2):
                    device_relationship.edgeType = 1
                else:
                    device_relationship.edgeType = 0
                device_relationship.save()

            if(rule.comparator == '<='):
                if(params_1 <= params_2):
                    device_relationship.edgeType = 1
                else:
                    device_relationship.edgeType = 0
                device_relationship.save()

            if(rule.comparator == '>='):
                if(params_1 >= params_2):
                    device_relationship.edgeType = 1
                else:
                    device_relationship.edgeType = 0
                device_relationship.save()
    return

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)