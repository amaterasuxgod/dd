from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from .models import OrderService, Services, UserBase, Order, Facility_type
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, OrderForm, GoodsOrderForm
from django.http.response import HttpResponse
# Create your views here.


def Contacts(request):
    return render(request, 'contacts.html')

def Adresses(request):
    facilities = Facility_type.objects.all()

    return render(request, 'adresses.html', {'adresses':facilities})


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
        orders = user_orders(request)
        return render(request, 'dashboard.html', {'orders': orders})
    else:
        return redirect('/home/login/')



class mainView(ListView):
    model = Services
    template_name = './main.html'


def ItemDetailView(request,pk):
    facilities = Facility_type.objects.all()
    services = Services.objects.get(id=pk)
    # tape = 'Пленка'
    # same_scene = OrderService.objects.filter(service='Пленка')
    if services.category == 'service':
        if request.method == 'POST':
            if request.user.is_authenticated:
                    user = UserBase.objects.get(user_name=request.user.user_name) 
                    selected_item = get_object_or_404(Facility_type, title=request.POST.get('item_id'))
                    orderForm = OrderForm(request.POST)                                    
                    if orderForm.is_valid():                                                                      
                        # created_order = Order.objects.order_by('id')[0]
                        order_service = orderForm.save(commit=False)
                        order_service.order = Order.objects.create(client=request.user)
                        order_service.service = services
                        order_service.urgency_rate = orderForm.cleaned_data['urgency_rate']
                        order_service.facility = selected_item
                        order_service.number_of_photos = orderForm.cleaned_data['number_of_photos']
                        order_service.paper_type = orderForm.cleaned_data['paper_type']
                        order_service.photo_format = orderForm.cleaned_data['photo_format']
                        if order_service.paper_type == 'Matte' or order_service.paper_type == 'Glossy' or order_service.paper_type == 'Semi-Glossy':
                            order_service.price = services.regular_price*1.1 * order_service.number_of_photos
                        if order_service.paper_type == 'SuperGlossy' or order_service.paper_type == 'Silk' or order_service.paper_type == 'Satin':
                            order_service.price = services.regular_price*1.2 * order_service.number_of_photos
                        if order_service.photo_format == '10x15' or order_service.photo_format == '9x12':
                            order_service.price = order_service.price * 1.1
                        if order_service.photo_format == '15x20' or order_service.photo_format == '15x22,5' or order_service.photo_format == '11,5x15':
                            order_service.price = order_service.price * 1.2
                        if order_service.photo_format == '21x30' or order_service.photo_format == '10x30' or order_service.photo_format == '15x45':
                            order_service.price = order_service.price * 1.3
                        if order_service.photo_format == '20x30':
                            order_service.price = order_service.price * 1.6
                        if order_service.photo_format == '30x40' or order_service.photo_format == '30x42' or order_service.photo_format == '30x45':
                            order_service.price = order_service.price * 1.8
                        if order_service.urgency_rate < 3:
                            order_service.price = order_service.price * 2
                        if order_service.number_of_photos>20:
                            order_service.price = order_service.price * 0.95
                        if services.title == 'Скидочная карта' and user.has_discount==False:
                            user.has_discount = True
                        if user.has_discount == True:
                            order_service.price = order_service.price * 0.90
                        if user.is_professional==True:
                            order_service.price = order_service.price * 0.90
                        rounded_price = round(order_service.price, 2)
                        order_service.price = rounded_price
                        # if same_scene:
                        #     for item in same_scene:
                        #         if item.facility == order_service.facility:
                        #             order_service.price = order_service.price * 0                                  
                        # else:
                        #     pass
                        user.save()
                        order_service.save()

                        return render(request, 'order_success.html', {'price': order_service.price})
                
                    else:
                        return HttpResponse('Validation error')

            else:
                return redirect('/home/login/')   
        else:
            orderForm = OrderForm()
        return render(request, 'service_detail.html', {'form': orderForm, 'services': services, 'facilities': facilities})
    
    else:
        if request.method == 'POST':
            if request.user.is_authenticated:
                user = UserBase.objects.get(user_name=request.user.user_name)
                selected_item = get_object_or_404(Facility_type, title=request.POST.get('item_id'))
                orderForm = GoodsOrderForm(request.POST)                                    
                if orderForm.is_valid():                                                                      
                    # created_order = Order.objects.order_by('id')[0]
                    order_service = orderForm.save(commit=False)
                    order_service.order = Order.objects.create(client=request.user)
                    order_service.service = services
                    order_service.facility = selected_item
                    order_service.number_of_photos = orderForm.cleaned_data['number_of_photos']
                    order_service.price = services.regular_price * order_service.number_of_photos
                    if services.title == 'Скидочная карта' and user.has_discount==False:
                        user.has_discount = True
                    if user.has_discount == True and services.title!='Скидочная карта':
                        order_service.price = order_service.price * 0.90
                    if user.is_professional==True:
                        order_service.price = order_service.price * 0.90
                    # orders = OrderService.objects.filter(facility='Филиал №1')       
                    # query = OrderService.objects.filter(order=orders)
                    # queryset = []
                    # queryset2 = []
                    # for item in orders:
                    #     queryset.append(item)
                    
                    # # for item in queryset:
                    # #     queryset2.append(OrderService.objects.get(order=item))

                    user.save()
                    order_service.save()

                    return render(request, 'order_success.html', {'price': order_service.price})
                
                else:
                    return HttpResponse('Validation error')
            else:
                return redirect('/home/login/')
        else:
            orderForm = GoodsOrderForm()
        return render(request, 'goods_detail.html', {'form': orderForm, 'services': services, 'facilities': facilities})    



def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(client=user_id)
    return orders