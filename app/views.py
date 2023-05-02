"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import OrderForm, FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog, Comment
from .forms import CommentForm, BlogForm # использование формы ввода комментария

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Мои контакты',
            'message':'Мои контакты',
            'year':datetime.now().year,
        }
    )
def video(request):
    """Renders the page with video."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/video.html',
        {
            'title':'Полезные видео',
            'message':'Полезные видео',
            'year':datetime.now().year,
        }
    )
def blog(request):
    """Renders the blog page."""

    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
            {
                'title':'Блог',
                'posts': posts, # передача списка статей в шаблон веб-страницы
                'year':datetime.now().year,
            }
        )
def blogpost(request, parametr):
    """Renders the page with one post from blog."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post_id_id=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post_id = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'year':datetime.now().year,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы 
        }
    )
def newpost(request):
    """Renders the page to create a new post."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            blog_f.creation_date = datetime.now() # добавляем в модель  текущую дату
            blog_f.date_of_change = datetime.now() # добавляем в модель  текущую дату
            blog_f.is_published = True
            blog_f.save() # сохраняем изменения после добавления полей
            return redirect('blog') # переадресация на ту же страницу статьи после отправки комментария
    else:
        blogform = BlogForm() # создание формы для ввода комментария
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform, # передача конкретной статьи в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year':datetime.now().year,
        }
    )
def shop(request):
    """Renders the shop page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/shop.html',
        {
            'title':'Магазин',
            'message':'Страница созданная для монетизации моего творчества.',
            'year':datetime.now().year,
        }
    )
def order(request):
    """Renders the order page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = dict()
            data['username'] = form.cleaned_data['username']
            data['age'] = form.cleaned_data['age']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            data['email'] = form.cleaned_data['email']
            data['phone'] = form.cleaned_data['phone']
            data['address'] = form.cleaned_data['address']
            data['date'] = form.cleaned_data['date']
            data['description'] = form.cleaned_data['description']
            form = None
    else: 
        form = OrderForm()
    return render(
        request,
        'app/order.html',
        {
            'form':form,
            'data':data,
            'title':'Оформить заказ',
            'message':'Заполните форму для оформления заказа.',
            'year':datetime.now().year,
        }
    )
def feedback(request):
    """Renders the feedback page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    likes = {
        '1': 'Очень нравится!',
        '2': 'Нравится, но нужно доработать.',
        '3': 'Сайт неплохой.',
        '4': 'Не нравится, нужно много поменять.',
        '5': 'Отвратительный сайт. Больше здесь не появлюсь!'
        }
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['age'] = form.cleaned_data['age']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            data['email'] = form.cleaned_data['email']
            if (form.cleaned_data['subscribe']== True):
                data['subscribe'] = 'Да'
            else:
                data['subscribe'] = 'Нет'
            data['likes'] = likes[ form.cleaned_data['likes'] ]
            data['message'] = form.cleaned_data['message']
            form = None
    else: 
        form = FeedbackForm()
    return render(
        request,
        'app/feedback.html',
        {
            'form':form,
            'data':data,
            'title':'Оставить отзыв о сайте',
            'message':'Заполните форму обратной связи:',
            'year':datetime.now().year,
        }
    )


def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )
