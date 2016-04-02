from django.shortcuts import render_to_response, render
from django.http import HttpResponse, JsonResponse
from django import forms
from plan_surgery.models import Device, Surgery
from collections import defaultdict

import re
import json
import code
import urllib
import requests
from IPython import embed

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
        results[device.product_type].append((device.manufacturer, device.brand_name, device.description, dims, device.notes, links, device.id))
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
        results['name'].append((str(device.product_type), device.manufacturer, device.brand_name, device.description, dims, device.id))
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
    context = {"devices" : devices}
    return render(request, 'plan_surgery/all.html', context)

def show(request, id, message=""):
    device = Device.objects.get(pk=id)
    links = None
    if device.useful_links:
        links = [str(x).replace('watch?v=', 'v/') for x in json.loads(device.useful_links)]
    context = {"manufacturer": device.manufacturer, "brand_name": device.brand_name, "description": device.description, "product_type": device.product_type, "id": id, "notes": device.notes, "useful_links": links, "message": message}
    return render(request, 'plan_surgery/show.html', context)

def add_video(request, id):
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

