from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):

    # RSS elements
    title = 'My Blog'
    link = reverse_lazy('blog:post-list')
    description = 'New Posts of my blog'

    def items(self):
        return Post.publishedPosts.all()[:5]
    
    def item_title(self, item) :
        return item.title
    
    def item_description(self, item) -> str:
        return truncatewords(item.body, 30)
