from django.shortcuts import render_to_response, render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'plan_surgery/index.html', {})
