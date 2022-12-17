from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', Registration.as_view(), name='registration'),
    path('private/', Private.as_view(), name='private'),
    path('orders/', Orders.as_view(), name='orders'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
    path('category/<slug:category_slug>/', ShowCategory.as_view(), name='category'),
    path('contact/', Contact.as_view(), name='contact'),
    path('contact/thank_you/', ContactFeedback.as_view(), name='contact_feedback'),
    path('page_not_found/', page_not_found, name='page_not_found'),
    path('search/', Search.as_view(), name='search'),
]


# cache_page(60)()
