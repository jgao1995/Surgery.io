from django.shortcuts import render_to_response, render
from django.http import HttpResponse
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

