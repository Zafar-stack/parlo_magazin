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


