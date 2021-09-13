from django.urls import path 
from . import views

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
]
