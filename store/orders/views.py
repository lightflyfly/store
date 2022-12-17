from django.shortcuts import render, redirect
from app.models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.login = request.user
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                cart.clear()
                return render(request, 'orders/created.html', {'title': 'Заказ оформлен', 'order': order})
        else:
            form = OrderCreateForm
        return render(request, 'orders/create.html', {'title': 'Оформление заказа', 'cart': cart, 'form': form})
    else:
        return redirect("login")
