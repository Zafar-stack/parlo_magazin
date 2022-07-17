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

    if search_value:
        goods = Good.objects.filter(category__id=catalog_id).filter(title__contains=search_value)

    return render(request, 'catalog.html', {'categories': categories,
                                            'goods': goods,
                                            'brands': brands,
                                            'colors': colors,
                                            'sizes': sizes,
                                            'tags': tags,
                                            'active_category': active_category,
                                            'search_value': search_value,
                                            })


