from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from django.db.models import F
from .forms import PostAddForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout

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
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()  # Создание и сохранение объекта Post
            return redirect('post_detail', pk=post.pk)  # Перенаправление на страницу созданной статьи
    else:
        form = PostAddForm()

    context = {
        'form': form,
        'title': 'Добавить статью'
    }
    return render(request, 'cooking/article_add_form.html', context)

def user_login(request):
    """Аутентификация пользователя"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }

    return render(request, 'cooking/login_form.html', context)

def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }

    return render(request, 'cooking/register_form.html', context)