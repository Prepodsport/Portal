from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchPosts.as_view(), name='search_posts'),
    path('search/posts/', views.Search.as_view(), name='search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path("categories/<int:pk>", CategoriesView.as_view(), name='categories_list'),
    path('categories/<int:pk>/subscribe/', add_me_to_category, name='sub_category'),
    path('categories/<int:pk>/unsubscribe/', delete_me_to_category, name='un_sub_category'),
    path('categories/', cache_page(60 * 5)(CategoryListView.as_view()), name='category_lists'),
]
