from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Services
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.http.response import HttpResponse
# Create your views here.


def Contacts(request):
    return render(request, 'contacts.html')

def Adresses(request):
    return render(request, 'adresses.html')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            return render(request, 'main.html')
    
    return render(request, 'account/registration/register.html', {'form': registerForm})




class mainView(ListView):
    model = Services
    template_name = './main.html'