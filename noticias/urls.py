from django.urls import path
from .views import create_article

urlpatterns = [
    path('create/', create_article, name='create_article'),
     #path('list/', views.ArticleListView.as_view(), name='article_list'),
]
