from django import forms
from .models import OrderService, UserBase, Facility_type, Order_photo


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Введите имя пользователя', min_length=4, max_length=50, help_text='Обязательно')
    email = forms.EmailField(max_length=100, help_text='Обязательно', error_messages={'required': 'Простите, требуется ввести email'})
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', )               

    
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Такой пользователь уже существует")
        return user_name
    
    def check_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return data['password2']
    
    def email_check(self):
        email = self.cleaned_data['email']
        email = UserBase.objects.filter(email=email)
        if email.count():
            raise forms.ValidationError('Данный email уже привязан к аккаунту')
        return email


class OrderForm(forms.ModelForm):

    PAPER_TYPE_CHOICE  =(
    ("Matte (Матовая)", "Matte (Матовая)"),
    ("Glossy (Глянцевая)", "Glossy (Глянцевая)"),
    ("Semi-Glossy (Полуглянцевая)", "Semi-Glossy (Полуглянцевая)"),
    ("SuperGlossy (Сверхглянцевая)", "SuperGlossy (Сверхглянцевая)"),
    ("Silk (Шелковая)", "Silk (Шелковая)"),
    ("Satin (Атласная)", "Satin (Атласная)"),
)

    PHOTO_FORMAT_CHOICE  =(
    ("10x15", "10x15"),
    ("15x20", "15x20"),
    ("21x30", "21x30"),
    ("9x12", "9x12"),
    ("11,5x15", "11,5x15"),
    ("15x22,5", "15x22,5"),
    ("10x30", "10x30"),
    ("15x45", "15x45"),
    ("20x30", "20x30"),
    ("30x40", "30x40"),
    ("30x42", "30x42"),
    ("30x45", "30x45"),
)




    urgency_rate = forms.IntegerField(label='Введите срочность заказа (в днях)')
    paper_type = forms.ChoiceField(label='Введите тип бумаги', choices=PAPER_TYPE_CHOICE)
    photo_format =  forms.ChoiceField(label='Введите формат фото', choices=PHOTO_FORMAT_CHOICE)
    class Meta:
        model = OrderService
        fields = ('urgency_rate', 'paper_type', 'photo_format')



class GoodsOrderForm(forms.ModelForm):

    number_of_photos = forms.IntegerField(label='Введите количество')
    class Meta:
        model = OrderService
        fields = ('number_of_photos',)  