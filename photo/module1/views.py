from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Services, UserBase, Order
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, OrderForm
from django.http.response import HttpResponse
# Create your views here.


def Contacts(request):
    return render(request, 'contacts.html')

def Adresses(request):
    return render(request, 'adresses.html')


def Goods_by_category(request):
    goods = Services.objects.filter(category='good')
    context = {"goods": goods}
    return render(request, 'goods_by_category.html', context)



def Services_by_category(request):
    services = Services.objects.filter(category='service')
    context = {"services": services}
    return render(request, 'services_by_category.html', context)


def account_register(request):

    if request.user.is_authenticated:
        return redirect('/home/homepage/')
    
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            return render(request, 'main.html')
    
    else:
        registerForm = RegistrationForm()
    return render(request, 'register.html', {'form': registerForm})



def DashboardView(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return redirect('/home/login/')



class mainView(ListView):
    model = Services
    template_name = './main.html'


def ItemDetailView(request,pk):
    services = Services.objects.get(id=pk)
    if request.method == 'POST':
        orderForm = OrderForm(request.POST)
        if orderForm.is_valid():
            order = Order.objects.create(client=request.user)
            order_service = orderForm.save(commit=False)
            order_service.order = order.id
            order_service.service = services.id
            order_service.urgency_rate = orderForm.cleaned_data['urgency_rate']
            order_service.facility = orderForm.cleaned_data['facility']
            order_service.number_of_photos = orderForm.cleaned_data['number_of_photos']
            order_service.paper_type = orderForm.cleaned_data['paper_type']
            order_service.photo_format = orderForm.cleaned_data['photo_format']
            order_service.save()

            return render(request, 'order_success.html')
    
    else:
        orderForm = OrderForm()
    return render(request, 'service_detail.html', {'form': orderForm, 'services': services})