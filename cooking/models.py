from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категория новостей"""
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для просмотра деталей категории"""
        return reverse('category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    """Для новостных постов"""
    title = models.CharField(max_length=255, verbose_name='Заголовок статьи')
    content = models.TextField(default='Скоро тут будет статья ....', verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    watched = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для просмотра деталей статьи"""
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'