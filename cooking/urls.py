from django.urls import path, include
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>/', category_list, name='category_list'),
    path('post/<int:pk>/', post_detail, name='post_detail')
]