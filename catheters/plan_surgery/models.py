from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from jsonfield import JSONField

import json

# Create your models here.

class DeviceType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fields = models.CharField(max_length=1000) # JSON LIST of STRINGS
    def __str__(self):
        return self.name

class TypeDependency(models.Model):
    # DeviceType 1 [foreign key], DeviceType 2 [foreign key], field1[str], field2[str], comparator[str]
    device_type_1 = models.ForeignKey(DeviceType, related_name='device_type_1_typedependency')
    device_type_2 = models.ForeignKey(DeviceType, related_name='device_type_2_typedependency')
    field_1 = models.CharField(max_length=200)
    field_2 = models.CharField(max_length=200)
    comparator = models.CharField(max_length=2)


class Device(models.Model):
    manufacturer = models.CharField(max_length=500)
    brand_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    # product_type = models.CharField(max_length=200)

    notes = models.TextField(null=True)
    useful_links = models.CharField(max_length=2000, null=True) # JSON
    product_type = models.ForeignKey(DeviceType)

    dimensions = JSONField()

    def __str__(self):
        return '<Device> {1} | {0} | {3} | {2}'.format(self.manufacturer, self.brand_name, self.description, self.product_type)


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
    device_1 = models.ForeignKey(Device, related_name='device1_device')
    device_2 = models.ForeignKey(Device, related_name='device2_device')
    edgeType = models.IntegerField()

    def __str__(self):
        return '{0} to {1} has dependency {2}'.format(self.device_1, self.device_2, self.edgeType)


def createDependencies():
    devices = Device.objects.all()
    # for each device, look at the relationship with every other device
    for device in devices:
        for other in devices:
            # look in the rules graph for the right rule
            rules = TypeDependency.objects.filter(device_type_1 = device.product_type, device_type_2 = other.product_type)
            if len(rules) < 1:
                dependence = DeviceDependency(device_1 = device, device_2 = other, edgeType = 0)
                dependence.save()
                print "Invalid Rule Graph"
                continue
            # get the rule out
            rule = rules[0]
            # parse the fields to compare out of each
            dims_1 = getattr(device, 'dimensions', None)
            dims_2 = getattr(other, 'dimensions', None)
            if not (dims_1 and dims_2):
                print 'invalid: no dimensions for either'
            params_1 = json.loads(dims_1)[rule.field_1]
            params_2 = json.loads(dims_2)[rule.field_2]
            edge = 0
            if rule.comparator == '<':
                if params_1 < params_2:
                    edge = 1
            if rule.comparator == '>':
                if params_1 > params_2:
                    edge = 1
            if rule.comparator == '=':
                if params_1 == params_2:
                    edge = 1
            if rule.comparator == '<=':
                if params_1 <= params_2:
                    edge = 1
            if rule.comparator == '>=':
                if params_1 >= params_2:
                    edge = 1
            dependence = DeviceDependency(device_1 = device, device_2 = other, edgeType = edge)
            dependence.save()


def updateDependencies():

    devices = Device.objects.all()
    # for each device, look at the relationship with every other device
    for device in devices:
        for other in devices:
            # look in the rules graph for the right rule
            rules = TypeDependency.objects.filter(device_type_1 = device.product_type, device_type_2 = other.product_type)
            if len(rules) < 1:
                # dependence = DeviceDependency(device_1 = device, device_2 = other, edgeType = 0)

                print "Invalid Rule Graph"
                continue
            dependence = DeviceDependency.filter(device_1 = device, device_2 = other)[0]
            # get the rule out
            rule = rules[0]
            # parse the fields to compare out of each
            dims_1 = getattr(device, 'dimensions', None)
            dims_2 = getattr(other, 'dimensions', None)
            if not (dims_1 and dims_2):
                print 'invalid: no dimensions for either'
            params_1 = json.loads(dims_1)[rule.field_1]
            params_2 = json.loads(dims_2)[rule.field_2]
            edge = 0
            if rule.comparator == '<':
                if params_1 < params_2:
                    edge = 1
            if rule.comparator == '>':
                if params_1 > params_2:
                    edge = 1
            if rule.comparator == '=':
                if params_1 == params_2:
                    edge = 1
            if rule.comparator == '<=':
                if params_1 <= params_2:
                    edge = 1
            if rule.comparator == '>=':
                if params_1 >= params_2:
                    edge = 1
            dependence.edgeType = edge
            dependence.save()


#### GRAPH DATABASE ####



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
    dependency.save()


def create_dummy_devices():
    wire = DeviceType.objects.filter(name='Wire')[0]
    wire1 = Device(manufacturer='man', brand_name='wire_brand', description='dummy wire', product_type=wire, dimensions='{"thickness": 10}')
    catheter = DeviceType.objects.filter(name='Catheter')[0]
    catheter2 = Device(manufacturer='cath', brand_name='cath_brand', description='dummy catheter', product_type=catheter, dimensions='{"min_inner_diameter": 15}')
    wire1.save()
    catheter2.save()
    return (wire1, catheter2)

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



def seed_db():
    # seeds the db
    createDummyDependency()
    wire1, catheter2 = create_dummy_devices()









