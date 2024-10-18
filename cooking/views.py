from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from django.db.models import F
from .forms import PostAddForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

class Index(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {'title': 'Главная страница'}

# def category_list(request, pk):
#     """Реакция на нажатие кнопки"""
#     category = get_object_or_404(Category, pk=pk)
#     posts = Post.objects.filter(category=category)  
   
#     context = {
#         'title': category.title,  # Используем поле title для названия категории
#         'posts': posts,
#     }
#     return render(request, 'cooking/index.html', context)

class ArticleByCategory(Index):
   """Реакция на нажатие кнопки"""
   def get_queryset(self):
    """Здесь можно изменить фильтрацию"""
    return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data() ###context[] ={}
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


# def post_detail(request, pk):
#     """Страница статьи"""
#     article = get_object_or_404(Post, pk=pk)
#     article.watched = F('watched') + 1  # Обновляем счетчик просмотров
#     article.save()
#     ext_post = Post.objects.exclude(pk=pk).order_by('-watched')[:5]
#     context = {
#         'title': article.title,
#         'post': article,
#         'ext_posts': ext_post
#     }
#     return render(request, 'cooking/article_detail.html', context)

class PostDetail(DetailView):
    """Страница статьи"""
    model = Post
    template_name = 'cooking/article_detail.html'

    def get_queryset(self):
        """Здесь можно делать доп.фильтрацию"""
        return Post.objects.filter(pk=self.kwargs['pk'])

        def get_context_data(self, **kwargs):
            """Для динамических данных"""
            Post.objects.filter(pk=self.kwargs['pk']).update(watched=F('watched') + 1)
            context = super().get_contxt_data()
            post = Post.objects.get(pk=self.kwargs['pk'])
            posts = Post.objects.exclude(pk=self.kwargs['pk']).order_by('-watched')[:5]
            context['title'] = post.title
            context['ext_posts'] = posts
            return context


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
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в аккаунт')
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль')
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
            return redirect('login')  # Перенаправление на страницу входа после регистрации
    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }

    return render(request, 'cooking/register_form.html', context)