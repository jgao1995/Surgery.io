from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django import forms
from plan_surgery.models import Device, Surgery
from collections import defaultdict

class NameForm(forms.Form):
    your_name = forms.CharField(label='Enter catheter name ', max_length=100)

# Create your views here.
def index(request):

    context = { "form" : NameForm() }
    return render(request, 'plan_surgery/index.html', context)

def search(request):
    query = request.GET['query']
    query_set = Device.objects.filter(manufacturer__contains=query) | Device.objects.filter(brand_name__contains=query) | Device.objects.filter(description__contains=query)
    results = defaultdict(list)
    for device in query_set:
        results[device.product_type].append((device.manufacturer, device.brand_name, device.description, device.dimensions))
    context = {'results': dict(results)}
    return render(request, 'plan_surgery/search_results.html', context)

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
