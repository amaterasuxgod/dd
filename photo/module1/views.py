from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Services
# Create your views here.


def Contacts(request):
    return render(request, 'contacts.html')

def Adresses(request):
    return render(request, 'adresses.html')

class mainView(ListView):
    model = Services
    template_name = './main.html'