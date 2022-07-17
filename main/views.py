from django.shortcuts import render
from main.models import *

# Create your views here.


def indexHandler(request):
    categories = Category.objects.all()

    return render(request, 'index-3.html', {'categories': categories,

                                            })


def catalogHandler(request):
    categories = Category.objects.all()

    return render(request, 'catalog.html', {'categories': categories,

                                            })


def catalogItemHandler(request, catalog_id):
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

    if search_value:
        new_goods = []
        for g in goods:
            if g.title.find(search_value) > -1:
                new_goods.append(g)
        goods = new_goods

    if active_brands:
        new_goods = []
        for g in goods:
            if g.brand and str(g.brand.id) in active_brands:
                new_goods.append(g)
        goods = new_goods

    if active_colors:
        new_goods = []
        for g in goods:
            if g.color and g.color.id in active_brands:
                new_goods.append(g)
        goods = new_goods

    if active_sizes:
        new_goods = []
        for g in goods:
            if g.size and g.size.id in active_sizes:
                new_goods.append(g)
        goods = new_goods

    return render(request, 'catalog.html', {'categories': categories,
                                            'goods': goods,
                                            'brands': brands,
                                            'colors': colors,
                                            'sizes': sizes,
                                            'tags': tags,
                                            'active_category': active_category,
                                            'search_value': search_value,
                                            'active_brands': active_brands,
                                            'active_colors': active_colors,
                                            'active_sizes': active_sizes,
                                            })


