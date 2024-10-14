from django.shortcuts import render, get_object_or_404
from .models import Category, Post


def index(request):
    """Для главной страницы"""
    posts = Post.objects.all()  ##SELECT * FROM post
    
    context = {
        'title': 'Главная страница',
        'posts': posts,
    }
    return render(request, 'cooking/index.html', context)


def category_list(request, pk):
    """Реакция на нажатие кнопки"""
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category)  
   
    context = {
        'title': category.title,
        'posts': posts,
    }
    return render(request, 'cooking/index.html', context)


def post_detail(request, pk):
    """Страница статьи"""
    article = get_object_or_404(Post, pk=pk)
    context = {
        'title': article.title,
        'post': article
    }
    return render(request, 'cooking/article_detail.html', context)