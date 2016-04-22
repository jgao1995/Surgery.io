from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from jsonfield import JSONField

import json

class DeviceType(models.Model):
    '''
    model for specific type of device; e.g. Catheter, Wire
    name: name of Model e.g. "Catheter"
    fields: JSON list of strings e.g. "['min_inner_diameter']"
    '''
    name = models.CharField(max_length=200, unique=True)
    fields = models.CharField(max_length=1000) # JSON LIST of STRINGS
    def __str__(self):
        return self.name

class TypeDependency(models.Model):
    '''
    model to specify a relationship between DeviceTypes.

    DeviceType 1: foreign key (DeviceType)
    DeviceType 2: foreign key (DeviceType)
    field_1: str
    field_2: str
    comparator: str

    For example, catheter.min_inner_diameter > wire.max_outer_diameter:
        device_type_1 = Catheter
        device_type_2 = Wire
        field_1 = "min_inner_diameter"
        field_2 = "max_outer_diameter"
        comparator = ">"
    '''
    device_type_1 = models.ForeignKey(DeviceType, related_name='device_type_1_typedependency')
    device_type_2 = models.ForeignKey(DeviceType, related_name='device_type_2_typedependency')
    field_1 = models.CharField(max_length=200)
    field_2 = models.CharField(max_length=200)
    comparator = models.CharField(max_length=2)


class Device(models.Model):
    '''
    model to specify a particular instance of a Device Type.

    manufacturer: str
    brand_name: str
    description: str

    notes: str
    useful_links: str (JSON str of list)
    product_type: DeviceType [foreign key]
    dimensions: str (JSON str of object)
    remaining_dimensions: str (JSON str of object)
    '''
    manufacturer = models.CharField(max_length=500)
    brand_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    notes = models.TextField(blank=True, null=True)
    useful_links = models.CharField(max_length=2000, blank=True, null=True) # JSON
    product_type = models.ForeignKey(DeviceType)

    dimensions = JSONField()
    
    def __str__(self):
        return '<Device> {1} | {0} | {3} | {2}'.format(self.manufacturer, self.brand_name, self.description, self.product_type)


class Surgery(models.Model):
    '''
    model to represent specific Surgery.
    A surgery has many Devices, and a created_date.
    remaining_dimensions is a dictionary key=[Device id] => val={dim name => remaining space of dimension of device}
    May want to add creator
    '''
    devices = models.ManyToManyField(Device)
    remaining_dimensions =  JSONField()
    created_date = models.DateTimeField(default=timezone.now)

def add_device_to_database(manufacturer, brand_name, description, product_type, dims=None):
    '''
    manufacturer: str
    brand_name: str
    description: str
    product_type: DeviceType
    dims: str
    return true/false if it works out or not.'''
    dimensions = dims or {}
    # unit conversion??
    device = Device(manufacturer=manufacturer, brand_name=brand_name, description=description, dimensions=json.dumps(dimensions), remaining_dimensions=json.dumps(dimensions))

    return device.save()

def create_surgery():
    '''
    creates a sample Surgery and saves it.

    rtype: Surgery
    '''
    surgery = Surgery()
    surgery.save()
    return surgery

def add_device_to_surgery(device_in, device_into):
    # Assume device has been saved.
    # Check the dependency
    if DeviceDependency.get(device_1=device_into, device_2=device_in) == 1:
        surgery.devices.add(device_in)
        return device
    return None

class DeviceDependency(models.Model):
    '''
    model to represent dependency between two specific Devices (instances of DeviceType)
    device_1: Device
    device_2: Device
    edgeType: int [0/1]
        0: no relation between 2 devices
        1: relation between 2 devices
    '''
    device_1 = models.ForeignKey(Device, related_name='device1_device')
    device_2 = models.ForeignKey(Device, related_name='device2_device')
    edgeType = models.IntegerField()

    def __str__(self):
        return '{0} to {1} has dependency {2}'.format(self.device_1, self.device_2, self.edgeType)

def update(device_into, device_in):
    # TO DO
    return

def createDependencies():
    devices = Device.objects.all()
    # for each device, look at the relationship with every other device
    for device in devices:
        for other in devices:
            # look in the rules graph for the right rule
            rules = TypeDependency.objects.filter(device_type_1 = device.product_type, device_type_2 = other.product_type)
            rules2 = TypeDependency.objects.filter(device_type_2 = device.product_type, device_type_1 = other.product_type)
            if len(rules) < 1:
                # dependence = DeviceDependency(device_1 = device, device_2 = other, edgeType = 0)
                # dependence.save()
                continue
            dependencies = DeviceDependency.objects.filter(device_1=device, device_2=other)
            if len(dependencies) < 1:
                continue
            # get the rule out
            rule = rules[0]
            # parse the fields to compare out of each
            dims_1 = getattr(device, 'dimensions', None)
            dims_2 = getattr(other, 'dimensions', None)
            if not (dims_1 and dims_2):
                print 'invalid: no dimensions for either'
                continue
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
            if edge:
                dependence = DeviceDependency(device_1 = device, device_2 = other, edgeType = edge)
                dependence.save()
                print 'Saved dependency between',device,'and',other


def updateDependencies():
    '''
    Performs a mass update over all dependencies between devices, using the dependencies between DeviceTypes
    '''
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
            dims_1 = getattr(device, 'remaining_dimensions', None)
            dims_2 = getattr(other, 'remaining_dimensions', None)
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
    '''
    Creates new device type
    name: str
    fields: [str]
    '''
    field_str = json.dumps(fields)
    device_type = DeviceType(name=name, fields=field_str)
    return device_type

def create_dummy_dependency():
    '''
    creates dummy dependency between Device Types: Wire, Catheter
    '''
    wire = create_device_type('Wire', ['thickness', 'length'])
    catheter = create_device_type('Catheter', ['max_outer_diameter', 'min_inner_diameter', 'length'])
    wire.save()
    catheter.save()
    # new dependency between wire and catheter
    dependency = TypeDependency(device_type_1=wire, device_type_2=catheter, field_1='thickness', field_2='min_inner_diameter', comparator='<')
    dependency.save()


def create_dummy_devices():
    '''
    creates dummy devices: Wire, Catheter
    '''
    wire = DeviceType.objects.filter(name='Wire')[0]
    wire1 = Device(manufacturer='Mirage', brand_name='Mirage', description='Mirage wire', product_type=wire, dimensions='{"thickness": 0.008, "length": 200}')
    catheter = DeviceType.objects.filter(name='Catheter')[0]
    catheter2 = Device(manufacturer='ENVOY', brand_name='6F', description='Envoy catheter', product_type=catheter, dimensions='{"min_inner_diameter": 0.070, "max_outer_diameter": 0.078, "length":90100, "dead_space": 2.23}')
    wire1.save()
    catheter2.save()
    return (wire1, catheter2)

def create_dependency(type_1, type_2, field_1, field_2, comparator):
    '''
    Creates a TypeDependency between type_1 and type_2
    type_1: DeviceType
    type_2: DeviceType
    field_1: str
    field_2: str
    comparator: str
    '''
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
    ''' seeds the db with sample data for testing purposes'''
    createDummyDependency()
    wire1, catheter2 = create_dummy_devices()
    createDependencies()



