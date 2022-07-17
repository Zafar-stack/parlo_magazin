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
    categories = Category.objects.all()
    goods = Good.objects.filter(category__id=catalog_id)
    brands = CategoryBrand.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    tags = Tag.objects.all()

    return render(request, 'catalog.html', {'categories': categories,
                                            'goods': goods,
                                            'brands': brands,
                                            'colors': colors,
                                            'sizes': sizes,
                                            'tags': tags,
                                            })


