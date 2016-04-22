from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse, JsonResponse
from django import forms
from plan_surgery.models import Device, Surgery, createDependencies
from collections import defaultdict

import re
import json
import code
import urllib
import requests
from IPython import embed

class NameForm(forms.Form):
    your_name = forms.CharField(label='Enter catheter name ', max_length=100)


def compatibleDevices(catheter):
    '''
    Given a device, returns the compatible devices according to the rules defined in the Dependency database
    '''
    adjacency_list_1 = DeviceDependency.objects.filter(device_1=catheter)
    adjacency_list_2 = DeviceDependency.objects.filter(device_2=catheter)
    compatible = []
    for dependency in adjacency_list_1:
        if dependency.edgeType == 1:
            compatible.append(dependency.device_2)
    for dependency in adjacency_list_2:
        if dependency.edgeType == 1:
            compatible.append(dependency.device_1)
    return compatible

def search(request):
    '''
    Search function that returns results when you press the search button. Finds any devices 
    that have the query in their manufacturer, name, or description.
    '''
    query = request.GET['query']
    query_set = Device.objects.filter(manufacturer__contains=query) | Device.objects.filter(brand_name__contains=query) | Device.objects.filter(description__contains=query)
    results = defaultdict(list)
    for device in query_set:
        if isinstance(device.dimensions, unicode):
            dims = json.loads(device.dimensions)
        else:
            dims = device.dimensions[0]
        links = None
        if device.useful_links:
            links = [str(x).replace('watch?v=', 'v/') for x in json.loads(device.useful_links)]
        results[device.product_type].append((device.manufacturer, device.brand_name, device.description, dims, device.notes, links, device.id))
        print links
    context = {'results': dict(results)}
    return render(request, 'plan_surgery/search_results.html', context)


def dynamic_search(request):
    '''
    Method that returns a dictionary of matches for the query so far so that the frontend can display
    dynamic search suggestions
    '''
    query = request.GET['query']
    query_set = Device.objects.filter(manufacturer__contains=query) | Device.objects.filter(brand_name__contains=query) | Device.objects.filter(description__contains=query)
    results = defaultdict(list)
    for device in query_set:
        # code.interact(local=locals())
        if isinstance(device.dimensions, unicode):
            dims = json.loads(device.dimensions)
        else:
            dims = device.dimensions[0]
        results['name'].append((str(device.product_type), device.manufacturer, device.brand_name, device.description, dims, device.id))
    context = {'results': dict(results)}
    return JsonResponse({'results': dict(results)})

from plan_surgery.models import *

# Views are here.


def index(request):
    '''
    Renders the homepage 
    '''
    return render(request, 'index.html')


def plan_surgery(request):
    '''
    Renders the plan surgery page
    '''
    from django import forms
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Enter catheter name ', max_length=100)

    context = { "form" : NameForm() }
    return render(request, 'plan_surgery/index.html', context)
    

def all(request):
    '''
    Renders the all catheters page
    '''
    devices = Device.objects.all()      
    context = {"devices" : devices}
    return render(request, 'plan_surgery/all.html', context)
    
def show_add_device_1(request):
    '''
    Renders the add device page selecting devicetypes
    '''
    device_types = [x.name for x in DeviceType.objects.all()]
    context = {'types': device_types}
    return render(request, 'add_device.html', context)


def show_add_device_2(request):
    '''
    Renders the add device page part 2
    '''
    device_type_name = request.GET['dropdown']
    device_type = DeviceType.objects.filter(name=device_type_name)[0]
    fields = json.loads(device_type.fields)
    context = {'fields': fields, "device_type_name": device_type_name}
    return render(request, 'add_device_2.html', context)


def add_device(request):
    ''' receives post request for adding a device to the database'''
    device_type_name = request.POST['device_type']
    device_type = DeviceType.objects.filter(name=device_type_name)[0]
    fields = json.loads(device_type.fields)
    # embed(s)

    d = {}
    for field in fields:
        d[field] = request.POST[field]
    dimensions = json.dumps(d)
    manufacturer = request.POST['manufacturer']
    brand_name = request.POST['brand_name']
    description = request.POST['description']

    device = Device(manufacturer=manufacturer, brand_name=brand_name, description=description, dimensions=dimensions, product_type=device_type)
    device.save()

    # create new dependencies.
    createDependencies()

    return redirect('all')


def new_surgery(request):
    if request.method == "GET":
        return render(request, 'plan_surgery/new_surgery.html')
    else:
        new_surgery = Surgery()
        new_surgery.save()
        all_devices = Device.objects.all()
        context = {"devices": all_devices, "surgery": new_surgery}


# def add_device_to_surgery(request, id):
    # print("We here!")
    # device_id = request.GET['device']
    # device = Device.objects.get(pk=device_id) 
    # surgery = Surgery.objects.get(pk=id)
    # surgery.devices.add(device)
    # return JsonResponse({"code": "success"})

def show(request, id, message=""):
    '''
    Renders the show page for a given catheter ID
    '''
    device = Device.objects.get(pk=id)
    compatible = compatibleDevices(device)
    results = defaultdict(list)
    for dev in compatible:
        if isinstance(dev.dimensions, unicode):
            dev_dims = json.loads(dev.dimensions)
        else:
            dev_dims = dev.dimensions[0]
        results[dev.product_type].append((dev.manufacturer, dev.brand_name, dev.description, dev_dims, dev.id))
    links = None
    if device.useful_links:
        links = [str(x).replace('watch?v=', 'v/') for x in json.loads(device.useful_links)]
    if isinstance(device.dimensions, unicode):
        dims = json.loads(device.dimensions)
    else:
        dims = device.dimensions[0]
    context = {"compatible_devices": dict(results), "dimensions": dims, "manufacturer": device.manufacturer, "brand_name": device.brand_name, "description": device.description, "product_type": device.product_type, "id": id, "notes": device.notes, "useful_links": links, "message": message}
    return render(request, 'plan_surgery/show.html', context)
    

def add_video(request, id):
    '''
    Allows the user to add videos to a page through the add video button
    '''
    device = Device.objects.get(pk=id)
    useful_links = device.useful_links
    if (useful_links is None):
        links = []
    else:
        links = json.loads(device.useful_links)
    link = request.GET['url']
    link = urllib.unquote(link)
    link = link.encode('ascii', 'ignore')
    # verify that link works.
    p = re.compile('https?://(www.)?youtube.com/watch\?v=(.*)')
    m = p.match(link)
    # embed()
    if m:
        video_id = m.group(2)
        img_url = 'http://img.youtube.com/vi/{}/0.jpg'.format(video_id)
        r = requests.get(img_url)
        if r.status_code == 200:
            if link not in links:
                links.append(link)
            device.useful_links = json.dumps(links)
            device.save()
            return show(request, id, "Added video successfully.")
    return show(request, id, "Failed to add video. Please use a valid YouTube URL.")

    
def add_comment(request, id):
    '''
    Allows the user to add comments to a page through the add comment button
    '''
    device = Device.objects.get(pk=id)
    notes = request.GET['comment']
    current = device.notes
    if (current is None):
        current = ''
    current = current.encode('ascii', 'ignore')
    current = current + ' ' + notes + '\n'
    device.notes = current
    device.save()
    return show(request, id)

