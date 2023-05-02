"""
Definition of forms.
"""

from django import forms
import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS. Форма автоизации"""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


class OrderForm(forms.Form):
    """Форма отправки заявки на заказ"""
    username = forms.CharField(label='ФИО пользователя',
                               min_length=10,
                               max_length=100,
                               required=True,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'ФИО пользователя'})
                               )
    age = forms.IntegerField(label='Возраст',
                             required=True,
                             widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': '10'})
                             )
    gender = forms.ChoiceField(label='Пол',
                               choices=[('1', 'Мужской'),('2', 'Женский')],
                               widget=forms.RadioSelect, initial=2
                               )
    email = forms.EmailField(label='E-mail',
                             required=True,
                             min_length=10,
                             widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'example@mail.ru'})
                             )
    phone = forms.CharField(label='Номер телефона',
                             required=True,
                             min_length=11,
                             max_length=18,
                             widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': '+7 (900) 123-45-67'})
                             )
    address = forms.CharField(label='Адрес доставки',
                              required=True,
                                min_length=10,
                                max_length=300,
                                widget=forms.Textarea(attrs = {'rows': 3, 'cols': 20, 'class': 'form-control',
                                   'placeholder': 'Россия, г. Санкт-Петербург, Лиговский пр-т 64, кв. 12, эт. 2'}
                              )) 
    
    date = forms.DateField(label='Дата доставки',
                            initial=datetime.date.today,
                            widget=forms.SelectDateWidget(
                               empty_label = 'Дата доставки',
                               attrs = {
                                    'placeholder': 'Дата доставки',
                                    'class': 'form-select col-md-4 mx-2'
                                })
                            )
    description = forms.CharField(label='Описание пожеланий',
                               required=True,
                               min_length=10,
                               widget=forms.Textarea(attrs = {'rows': 5, 'cols': 20, 'class': 'form-control',
                                   'placeholder': 'Описание желаемой работы'},
                                   )
                               )
class FeedbackForm(forms.Form):
    """Форма отправки заявки на заказ"""
    name = forms.CharField(label='Имя',
                               min_length=3,
                               max_length=100,
                               required=True,
                               widget=forms.TextInput({
                                   
                                   'placeholder': 'Ваше имя'})
                               )
    age = forms.IntegerField(label='Возраст',
                             required=False,
                             widget=forms.TextInput({
                                   
                                   'placeholder': '20'})
                             )
    gender = forms.ChoiceField(label='Пол',
                               choices=[('1', 'Мужской'),('2', 'Женский')],
                               widget=forms.RadioSelect, initial=1
                               )
    email = forms.EmailField(label='E-mail',
                             required=True,
                             min_length=10,
                             widget=forms.TextInput({
                                   
                                   'placeholder': 'example@mail.ru'})
                             )
    subscribe = forms.BooleanField(label='Подписаться на новости по e-mail?',
                                  required=False)
    likes = forms.ChoiceField(label='Насколько вам нравится наш сайт',
                               choices=[('1', 'Очень нравится!'),
                                        ('2', 'Нравится, но нужно немного доработать.'),
                                        ('3', 'Сайт неплохой, но требуются доработки.'),
                                        ('4', 'Не нравится, нужно много поменять.'),
                                        ('5', 'Отвратительный сайт. Больше здесь не появлюсь!')
                                        ],
                               widget=forms.Select({
                                   'class': 'form-control-select',
                                   }),
                               initial=1
                               )

    """
    addtosite = forms.MultipleChoiceField(label='Что вам хотелось бы видеть на сайте',
                                          required=False,
                                          choices=[('1', 'Поисковую строку.'),
                                                    ('2', 'Меню навигации на сайте в целом.'),
                                                    ('3', 'Боковое меню навигации с категориями на странице магазина.'),
                                                    ('4', 'Страницу с полезными источниками.'),
                                                    ('5', 'Видеоуроки и другие видео.')
                                                    ],
                                          widget=forms.CheckboxSelectMultiple
                                         )
    """
    message = forms.CharField(label='Отзыв',
                               required=False,
                               min_length=10,
                               widget=forms.Textarea(attrs = {'rows': 5, 'cols': 20, 
                                   'placeholder': 'Ваш отзыв'},
                                   )
                               )

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text
    text = forms.CharField(label='Комментарий',
                 widget=forms.Textarea(attrs = {'rows': 5, 'cols': 20, 'class': 'form-control',
                                   'placeholder': 'Ваш комментарий...'},
                                   )
                               )


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog # используемая модель
        fields = ('title', 'description', 'content', 'category', 'snapshot') # требуется заполнить только поле text
        labels = {'title': "Заголовок поста" , 'description': "Краткое описание", 'content': "Содержание поста" ,'category': "Категория", 'snapshot': "Изображение"} # метка к полю формы text