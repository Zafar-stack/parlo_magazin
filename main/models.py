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
    level = models.IntegerField(max_length=280, blank=True, default=0)

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
        return f'{self.title}'


