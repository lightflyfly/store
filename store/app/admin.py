from django.contrib import admin
from .models import *


class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'available', 'created', 'updated')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('available', 'price')
    list_filter = ('available', 'created', 'updated')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ContactReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'reason', 'email', 'order_number', 'created', 'request_granted')
    list_display_links = ('id', 'email')
    list_editable = ('request_granted',)
    search_fields = ('name',)
    list_filter = ('request_granted', 'reason', 'created')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'first_name', 'last_name', 'phone', 'address', 'created', 'updated', 'status')
    list_display_links = ('id',)
    list_editable = ('status',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price', 'quantity')
    list_display_links = ('id',)


class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    list_display_links = ('id', 'status')


admin.site.register(Product, AppAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactReason, ContactReasonAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
