"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Контент')
    description = models.CharField(max_length=255, null=False, blank=False, verbose_name='Краткое описание')
    creation_date = models.DateTimeField(default=datetime.now(), verbose_name='Дата создания')
    date_of_change = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    snapshot = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")

    def get_absolute_url(self):
        return reverse('view_blog', args=[str(self.pk)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Posts'
        ordering = ['-creation_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты блога'

class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Comment(models.Model):
    text = models.TextField(blank=False, verbose_name='Комментарий')
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name='Дата добавления')
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post_id = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Пост')

    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post_id)

    class Meta:
        db_table='Comment'
        verbose_name = 'Комментарии к статье блога'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']

admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(Category)