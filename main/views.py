from django.shortcuts import render

# Create your views here.


def indexHandler(request):

    return render(request, 'index-3.html', {})


