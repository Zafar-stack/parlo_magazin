from django.db import models

# Create your models here.


class Color(models.Model):
    title = models.CharField(max_length=208, blank=True)
    code = models.CharField(max_length=280, blank=True)
    level = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=208, blank=True)
    code = models.CharField(max_length=280, blank=True)
    level = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.title} - {self.code}'


class Tag(models.Model):
    title = models.CharField(max_length=208, blank=True)
    level = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    title = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(default=0, blank=True)
    good_count = models.IntegerField(default=0, blank=True)
    sub_category_count = models.IntegerField(default=0, blank=True)
    logo = models.ImageField(upload_to='upload', blank=True)

    def __str__(self):
        result_title = self.title

        parent_model = self.parent
        while parent_model:
            result_title = parent_model.title + ' --> ' + result_title
            parent_model = parent_model.parent

        return result_title


class Good(models.Model):
    title = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    level = models.IntegerField(default=0, blank=True)
    old_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    rating = models.FloatField(default=0)
    mini_description = models.TextField(blank=True)
    color = models.ForeignKey("Color", on_delete=models.CASCADE)
    size = models.ForeignKey("Size", on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='upload', blank=True)
    logo2 = models.ImageField(upload_to='upload', blank=True)
    logo3 = models.ImageField(upload_to='upload', blank=True)
    logo4 = models.ImageField(upload_to='upload', blank=True)
    logo5 = models.ImageField(upload_to='upload', blank=True)
    logo6 = models.ImageField(upload_to='upload', blank=True)
    logo_vertical = models.ImageField(upload_to='upload', blank=True)
    logo_horizontal = models.ImageField(upload_to='upload', blank=True)
    description = models.TextField(blank=True)
    weight = models.TextField(blank=True)
    dimensions = models.TextField(blank=True)
    materials = models.TextField(blank=True)
    extra_info = models.TextField(blank=True)
    is_main = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_discount = models.BooleanField(default=False)
    #brand = models.ForeignKey(CategoryBrand, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.category} + "-->" + {self.title} + "-->" + {self.color.title} + "-->" + {self.size.title}'


