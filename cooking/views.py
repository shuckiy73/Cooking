from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from django.db.models import F
from .forms import PostAddForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy


class Index(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {'title': 'Главная страница'}


class ArticleByCategory(Index):
    """Реакция на нажатие кнопки"""
    def get_queryset(self):
        """Здесь можно изменить фильтрацию"""
        return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


class PostDetail(DetailView):
    """Страница статьи"""
    model = Post
    template_name = 'cooking/article_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data(**kwargs)
        Post.objects.filter(pk=self.kwargs['pk']).update(watched=F('watched') + 1)
        post = context['post']
        context['title'] = post.title
        context['ext_posts'] = Post.objects.exclude(pk=self.kwargs['pk']).order_by('-watched')[:5]
        return context


class AddPost(CreateView):
    """Добавление статьи без админки"""
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Добавить статью'}
    success_url = reverse_lazy('index')


class PostUpdate(UpdateView):
    """Изменение статьи по кнопке"""
    model = Post
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    success_url = reverse_lazy('index')


class PostDelete(DeleteView):
    """Удаление статьи"""
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'


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