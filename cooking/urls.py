from django.urls import path
from .views import (
    Index, ArticleByCategory, PostDetail, AddPost, PostUpdate, PostDelete,
    SearchResult, user_login, user_logout, register, add_comment, profile
)

urlpatterns = [
    # Главная страница
    path('', Index.as_view(), name='index'),

    # Список статей по категории
    path('category/<int:pk>/', ArticleByCategory.as_view(), name='category_list'),

    # Детали статьи
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),

    # Добавление статьи
    path('add_article/', AddPost.as_view(), name='add'),

    # Обновление статьи
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),

    # Удаление статьи
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    # Поиск статей
    path('search/', SearchResult.as_view(), name='search'),

    # Аутентификация пользователя
    path('login/', user_login, name='login'),

    # Выход пользователя
    path('logout/', user_logout, name='logout'),

    # Регистрация пользователя
    path('register/', register, name='register'),

    # Добавление комментария
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),

    # Профиль пользователя
    path('profile/<int:user_id>/', profile, name='profile'),
]