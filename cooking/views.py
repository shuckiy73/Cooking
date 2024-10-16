from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from django.db.models import F
from .forms import PostAddForm


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
    Post.objects.filter(pk=pk).update(watched=F('watched') + 1 )
    ext_post = Post.objects.all().order_by('-watched')[:5]
    context = {
        'title': article.title,
        'post': article,
        'ext_posts': ext_post
    }
    return render(request, 'cooking/article_detail.html', context)


def add_post(request):
    """Добавление статьи без админки"""
    if request.method == 'POST':
        pass
    else:
        form = PostAddForm()

    context = {
        'form': form,
        'title': 'Добавить статью'
    }
    return render(request, 'cooking/article_add_form.html', context)