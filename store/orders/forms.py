from django import forms
from app.models import Order


class OrderCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].label_suffix = ''

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон',
            'address': 'Адрес',
        }
