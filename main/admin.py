from django.contrib import admin
from main. models import *

# Register your models here.


class AdminModelSingle(admin.ModelAdmin):
    pass


admin.site.register(Color, AdminModelSingle)
admin.site.register(Size, AdminModelSingle)
admin.site.register(Tag, AdminModelSingle)