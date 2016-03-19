from django.shortcuts import render_to_response, render
from django.http import HttpResponse, JsonResponse
from django import forms
from plan_surgery.models import Device, Surgery
from collections import defaultdict
import json
import code

class NameForm(forms.Form):
    your_name = forms.CharField(label='Enter catheter name ', max_length=100)

# # Create your views here.
# def index(request):

#     context = { "form" : NameForm() }
#     return render(request, 'plan_surgery/index.html', context)

def search(request):
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
        # code.interact(local=locals())
        results[device.product_type].append((device.manufacturer, device.brand_name, device.description, dims, device.notes, links))
        print links
    context = {'results': dict(results)}
    return render(request, 'plan_surgery/search_results.html', context)

def dynamic_search(request):
    query = request.GET['query']
    query_set = Device.objects.filter(manufacturer__contains=query) | Device.objects.filter(brand_name__contains=query) | Device.objects.filter(description__contains=query)
    results = defaultdict(list)
    
    for device in query_set:
        # code.interact(local=locals())
        if isinstance(device.dimensions, unicode):
            dims = json.loads(device.dimensions)
        else:
            dims = device.dimensions[0]
        results['name'].append((device.product_type, device.manufacturer, device.brand_name, device.description, dims))
    context = {'results': dict(results)}
    return JsonResponse({'results': dict(results)})

from plan_surgery.models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def plan_surgery(request):
    from django import forms
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Enter catheter name ', max_length=100)

    context = { "form" : NameForm() }
    return render(request, 'plan_surgery/index.html', context)

def all(request):
	devices = Device.objects.all()
	device_strings = [str(d) for d in devices]
	context = {"devices" : device_strings}
	return render(request, 'plan_surgery/all.html', context)

def show(request, id):
    device = Device.objects.get(pk=id)
    context = {"manufacturer": device.manufacturer, "brand_name": device.brand_name, "description": device.description, "product_type": device.product_type}
    return render(request, 'plan_surgery/show.html', context)