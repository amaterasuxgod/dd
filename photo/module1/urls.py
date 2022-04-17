from django.urls import path
from .views import mainView, Contacts, Adresses

urlpatterns = [
    path('homepage/', mainView.as_view(), name='main'),
    path('contacts/', Contacts, name='contacts'),
    path('adresses/', Adresses, name='adresses')
]