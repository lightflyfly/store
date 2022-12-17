from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.shortcuts import render,  redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from cart.forms import *
from django.db.models import Q


# кэш - включить на последнем этапе разработки

# class Main(ListView):
#     model = Product
#     template_name = 'app/main.html'
#     context_object_name = 'products'
#     extra_context = {'title': 'Romaria Store'}
#     products = cache.get('products')
#     if not products:
#         products = Product.objects.filter(available=True)
#         cache.set('products', products, 60)
#
#     def get_queryset(self):
#         return self.products


class Main(ListView):
    model = Product
    template_name = 'app/main.html'
    context_object_name = 'products'
    extra_context = {'title': 'Romaria Store'}

    def get_queryset(self):
        return Product.objects.filter(available=True)


class ShowCategory(ListView):
    model = Product
    template_name = 'app/main.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'], available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['products'][0].category)
        return context


class Search(ListView):
    model = Product
    template_name = 'app/main.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск'
        return context


class ShowProduct(DetailView):
    model = Product
    template_name = 'app/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        context['cart_product_form'] = CartAddProductForm
        return context


class Contact(CreateView):
    form_class = ContactForm
    template_name = 'app/contact.html'
    success_url = reverse_lazy('contact_feedback')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Связаться с нами'
        return context


class Private(LoginRequiredMixin, TemplateView):
    template_name = 'app/private.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        return context


class Login(LoginView):
    form_class = LoginForm
    template_name = 'app/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('main')


class Registration(CreateView):
    form_class = RegisterUserForm
    template_name = 'app/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


def logout_user(request):
    logout(request)
    return redirect('login')


class Orders(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'app/orders.html'
    login_url = reverse_lazy('login')
    context_object_name = 'products'

    def get_queryset(self):
        base_orders = Order.objects.filter(login=self.request.user.username)
        orders = []
        products = []
        for bo in base_orders:
            orders.append(OrderItem.objects.filter(order=bo))
        for ord in orders:
            for o in ord:
                products.append(o)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказы'
        return context


class ContactFeedback(TemplateView):
    template_name = 'app/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Спасибо за обращение'
        return context


def page_not_found(request, *args, **kwargs):
    context = {'title': 'Страница не найдена'}
    response = render(request, "app/page_not_found.html", context=context)
    response.status_code = 404
    return response
