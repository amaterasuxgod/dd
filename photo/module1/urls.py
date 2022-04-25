from django.urls import path
from .views import mainView, Contacts, Adresses, account_register, ItemDetailView, Services_by_category, Goods_by_category
from django.contrib.auth import views as auth_views


app_name = 'module1'

urlpatterns = [
    path('homepage/', mainView.as_view(), name='main'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('contacts/', Contacts, name='contacts'),
    path('adresses/', Adresses, name='adresses'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('register/', account_register, name="account-register"),
    path('services_by_category/', Services_by_category, name="services-by-category"),
    path('goods_by_category/', Goods_by_category, name="goods-by-category"),
]