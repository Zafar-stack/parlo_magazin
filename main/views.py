from django.shortcuts import render
from main.models import *
from math import ceil
from django.shortcuts import redirect
from datetime import datetime

# Create your views here.


def indexHandler(request):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'index-3.html', {'categories': categories,
                                            'new_cart': new_cart,
                                            'cart_items': cart_items,

                                            })


def catalogHandler(request):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'catalog.html', {'categories': categories,
                                            'new_cart': new_cart,
                                            'cart_items': cart_items,

                                            })


def catalogItemHandler(request, catalog_id):
    new_cart = None
    cart_items = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    active_category = Category.objects.get(id=catalog_id)
    categories = Category.objects.all()
    goods = Good.objects.filter(category__id=catalog_id)
    brands = CategoryBrand.objects.filter(category__id=catalog_id)
    colors = Color.objects.filter(category__id=catalog_id)
    sizes = Size.objects.filter(category__id=catalog_id)
    tags = Tag.objects.all()
    search_value = request.GET.get('q', None)

    active_brands = request.GET.getlist('active_brand', [])
    active_brands = [int(i) for i in active_brands]

    active_colors = request.GET.getlist('active_color', [])
    active_colors = [int(i) for i in active_colors]

    active_sizes = request.GET.getlist('active_size', [])
    active_sizes = [int(i) for i in active_sizes]

    is_discount = request.GET.get('is_discount', None)
    is_new = request.GET.get('is_new', None)
    stock = request.GET.get('stock', None)

    price = request.GET.get('price', None)
    price_start, price_stop = None, None

    if price and len(price.split('-')) == 2:
        price_start = int(price.split('-')[0])
        price_stop = int(price.split('-')[1])

    if search_value:
        new_goods = []
        for g in goods:
            if g.title.find(search_value) > -1:
                new_goods.append(g)
        goods = new_goods

    if active_brands:
        new_goods = []
        for g in goods:
            if g.brand and g.brand.id in active_brands:
                new_goods.append(g)
        goods = new_goods

    if active_colors:
        new_goods = []
        for g in goods:
            if g.color and g.color.id in active_colors:
                new_goods.append(g)
        goods = new_goods

    if active_sizes:
        new_goods = []
        for g in goods:
            if g.size and g.size.id in active_sizes:
                new_goods.append(g)
        goods = new_goods

    if is_discount:
        new_goods = []
        for g in goods:
            if g.is_discount:
                new_goods.append(g)
        goods = new_goods

    if is_new:
        new_goods = []
        for g in goods:
            if g.is_new:
                new_goods.append(g)
        goods = new_goods

    if stock:
        new_goods = []
        for g in goods:
            if g.stock > 0:
                new_goods.append(g)
        goods = new_goods

    if price_start and price_stop:
        new_goods = []
        for g in goods:
            if g.price >= price_start and g.price <= price_stop:
                new_goods.append(g)
        goods = new_goods

    limit = request.GET.get('limit', 9)
    current_page = int(request.GET.get('page', 1))
    total = len(goods)
    pages_count = ceil(total / limit)
    pages = range(1, pages_count + 1)
    stop = current_page * limit
    start = stop - limit
    prev_page = current_page - 1
    next_page = None
    if current_page < pages_count:
        next_page = current_page + 1

    return render(request, 'catalog.html', {'categories': categories,
                                            'goods': goods[start:stop],
                                            'brands': brands,
                                            'colors': colors,
                                            'sizes': sizes,
                                            'tags': tags,
                                            'active_category': active_category,
                                            'search_value': search_value,
                                            'active_brands': active_brands,
                                            'active_colors': active_colors,
                                            'active_sizes': active_sizes,
                                            'is_discount': is_discount,
                                            'is_new': is_new,
                                            'stock': stock,
                                            'price': price,
                                            'pages': pages,
                                            'current_page': current_page,
                                            'prev_page': prev_page,
                                            'next_page': next_page,
                                            'total': total,
                                            'start': start,
                                            'stop': stop,
                                            'new_cart': new_cart,
                                            'cart_items': cart_items,
                                            })


def goodHandler(request, good_id):

    new_cart = None
    cart_items = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    categories = Category.objects.all()
    active_good = Good.objects.get(id=good_id)
    related_products = Good.objects.filter(category__id=active_good.category.id).exclude(id=good_id)

    return render(request, 'product-details.html', {'categories': categories,
                                                    'active_good': active_good,
                                                    'related_products': related_products,
                                                    'new_cart': new_cart,
                                                    'cart_items': cart_items,

                                                    })


def cartHandler(request):
    if not request.session.session_key:
        request.session.create()
    user_session_id = request.session.session_key

    categories = Category.objects.all()

    open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
    new_cart = None
    if open_carts:
        new_cart = open_carts[0]
    else:
        new_cart = Cart()
        new_cart.session_id = user_session_id
        new_cart.save()

    print('*'*100)
    print(new_cart)


    if request.POST:
        return_url = request.POST.get('return_url', '')
        action = request.POST.get('action', '')

        if action == 'add_to_cart':
            good_id = int(request.POST.get('good_id', 0))
            amount = float(request.POST.get('amount', 0))
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0).filter(good__id=good_id)
            print('*'*100)
            print(cart_items)

            if cart_items:
                new_cart_item = cart_items[0]
                new_cart_item.amount = new_cart_item.amount + amount
                new_cart_item.all_price = new_cart_item.price * new_cart_item.amount
                new_cart_item.save()
            else:
                new_cart_item = CartItem()
                new_cart_item.good_id = good_id
                new_cart_item.cart_id = new_cart.id
                new_cart_item.amount = amount
                new_cart_item.price = new_cart_item.good.price
                new_cart_item.all_price = new_cart_item.price * new_cart_item.amount
                new_cart_item.save()

        if action == 'remove_from_cart':
            good_id = int(request.POST.get('good_id', 0))
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0).filter(good__id=good_id)
            for ci in cart_items:
                ci.delete()

        if action == 'clear_cart':
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)
            for ci in cart_items:
                ci.delete()

        if action == 'checkout':
            new_cart.title = request.POST.get('title', '')
            new_cart.first_name = request.POST.get('first_name', '')
            new_cart.last_name = request.POST.get('last_name', '')
            new_cart.country = request.POST.get('country', '')
            new_cart.city = request.POST.get('city', '')
            new_cart.address = request.POST.get('address', '')
            new_cart.zip_code = request.POST.get('zip_code', '')
            new_cart.phone = request.POST.get('phone', '')
            new_cart.email = request.POST.get('email', '')
            new_cart.created_at = datetime.now()
            new_cart.status = 1
            new_cart.save()

        if action == 'accepted':
            order_id = int(request.POST.get('order_id', 0))
            if request.user.is_authenticated:
                main_order = Cart.objects.get(id=order_id)
                if main_order:
                    main_order.status = 2
                    main_order.save()

        if action == 'add_to_compare_list':
            good_id = int(request.POST.get('good_id', 0))
            compareItems = CompareItem.objects.filter(good__id=good_id).filter(session_id=user_session_id)
            if compareItems:
                pass
            else:
                compare_item = CompareItem()
                compare_item.session_id = user_session_id
                compare_item.good_id = good_id
                compare_item.save()

        if action == 'add_to_wish_list':
            good_id = int(request.POST.get('good_id', 0))
            wishItems = WishItem.objects.filter(good__id=good_id).filter(session_id=user_session_id)
            if wishItems:
                pass
            else:
                wish_item = WishItem()
                wish_item.session_id = user_session_id
                wish_item.good_id = good_id
                wish_item.save()

        if action == 'remove_from_compare_list':
            good_id = int(request.POST.get('good_id', 0))
            compare_items = CompareItem.objects.filter(good__id=good_id).filter(session_id=user_session_id)
            if compare_items:
                for ci in compare_items:
                    ci.delete()

        if action == 'remove_from_wish_list':
            good_id = int(request.POST.get('good_id', 0))
            wish_items = WishItem.objects.filter(good__id=good_id).filter(session_id=user_session_id)
            if wish_items:
                for ci in wish_items:
                    ci.delete()

        if action in ['add_to_cart', 'remove_from_cart', 'clear_cart']:
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)
            all_price = 0
            all_amount = 0
            all_orig_price = 0
            if cart_items:
                for ci in cart_items:
                    all_amount += ci.amount
                    all_orig_price += ci.amount * ci.price

            new_cart.orig_price = all_orig_price

            all_price = all_orig_price * (100 - new_cart.discount) / 100
            new_cart.amount = all_amount
            new_cart.orig_price = all_orig_price
            new_cart.price = all_price
            new_cart.save()

        if return_url:
            return redirect(return_url)

    cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'cart-page.html', {'new_cart': new_cart,
                                              'cart_items': cart_items,
                                              'categories': categories,

                                              })


def checkoutHandler(request):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'checkout.html', {'categories': categories,
                                            'new_cart': new_cart,
                                            'cart_items': cart_items,

                                            })


def checkoutsuccessHandler(request):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'checkout_success.html', {'categories': categories,
                                                     'new_cart': new_cart,
                                                     'cart_items': cart_items,

                                                     })


def ordersHandler(request):
    categories = Category.objects.all()
    new_cart = None
    cart_items = []
    confirmed_orders = []
    if request.user.is_authenticated:
        confirmed_orders = Cart.objects.filter(status__gte=1)

    return render(request, 'orders.html', {'categories': categories,
                                            'cart_items': [],
                                            'confirmed_orders': confirmed_orders,

                                            })


def ordersItemHandler(request, order_id):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []

    order_items = []
    if request.user.is_authenticated:
        order_items = CartItem.objects.filter(cart__id=order_id)
        main_order = Cart.objects.get(id=order_id)

    return render(request, 'order_item.html', {'categories': categories,
                                               'cart': new_cart,
                                               'cart_items': cart_items,
                                               'order_items': order_items,
                                               'main_order': main_order,

                                               })


def compareHandler(request):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []
    compare_list = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

        compare_list = CompareItem.objects.filter(session_id=user_session_id)


    return render(request, 'compare.html', {'categories': categories,
                                            'new_cart': new_cart,
                                            'cart_items': cart_items,
                                            'compare_list': compare_list,

                                            })


def wishHandler(request):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []
    wish_list = []

    user_session_id = request.session.session_key
    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

        wish_list = WishItem.objects.filter(session_id=user_session_id)

    return render(request, 'wish.html', {'categories': categories,
                                         'new_cart': new_cart,
                                         'cart_items': cart_items,
                                         'wish_list': wish_list,

                                         })


