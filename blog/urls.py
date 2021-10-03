from django.urls import path 
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('post_list/<slug:tag_slug>/', views.PostList.as_view(), name='post-list-with-tagging'),
    path('post_list/', views.PostList.as_view(), name='post-list'),
    path('post_detail/<int:year>/<int:month>/<int:day>/<slug:post>',
        views.post_detail,
        name='post-detail'
    ),
    path('<int:post_id>/share/',
        views.post_share,
        name='post-share'
    ),
    path('feed/', LatestPostsFeed(), name='blog-feed'),
    path('search/', views.post_search, name='post-search'),
    path('search_2/', views.post_search_2, name='post-search-2'),
    path('search_3/', views.post_search_3, name='post-search-3'),
    path('search_4/', views.post_search_4, name='post-search-4'),
]
