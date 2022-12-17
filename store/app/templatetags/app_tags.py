from django import template
from app.models import *

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_up_menu_logout():
    up_menu = [
        {'title': "Главная", 'url_name': 'main'},
        {'title': "Корзина", 'url_name': 'cart:cart_detail'},
        {'title': "Войти", 'url_name': 'login'},
    ]
    return up_menu


@register.simple_tag()
def get_up_menu_login():
    up_menu = [
        {'title': "Главная", 'url_name': 'main'},
        {'title': "Личный кабинет", 'url_name': 'private'},
        {'title': "Корзина", 'url_name': 'cart:cart_detail'},
        {'title': "Заказы", 'url_name': 'orders'},
    ]
    return up_menu


@register.simple_tag()
def get_down_menu():
    down_menu = [
        {'title': "Связаться с нами", 'url_name': 'contact'},
    ]
    return down_menu

