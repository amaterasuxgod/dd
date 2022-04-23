from django.urls import path
from .views import mainView, Contacts, Adresses, account_register
from django.contrib.auth import views as auth_views


app_name = 'module1'

urlpatterns = [
    path('homepage/', mainView.as_view(), name='main'),
    path('contacts/', Contacts, name='contacts'),
    path('adresses/', Adresses, name='adresses'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('register/', account_register, name="account-register"),
]