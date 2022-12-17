from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].empty_label = 'не выбрано'
        self.fields['order_number'].required = False
        self.fields['order_number'].initial = ''

        for f in self.fields:
            self.fields[f].label_suffix = ''

    class Meta:
        model = Contact
        fields = ['client_name', 'reason', 'content', 'email', 'order_number']
        labels = {
            'client_name': 'Имя',
            'reason': 'Я хочу',
            'content': 'Сообщение',
            'email': 'Email для ответа',
            'order_number': 'Номер заказа, если он есть',
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
