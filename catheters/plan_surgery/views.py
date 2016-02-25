from django.shortcuts import render_to_response, render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def plan_surgery(request):
  from django import forms
  class NameForm(forms.Form):
      your_name = forms.CharField(label='Enter catheter name ', max_length=100)

  context = { "form" : NameForm() }
  return render(request, 'plan_surgery/index.html', context)
