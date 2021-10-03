from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


from ..models import Post


register = template.Library()

@register.simple_tag
def total_posts() -> int: 
    return Post.publishedPosts.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count = 5):
    latest_posts = Post.publishedPosts.order_by('-published')[:count]
    return {'latest_posts':latest_posts}


@register.simple_tag()
def get_most_commented_posts(count: int = 5):
    return Post.publishedPosts.annotate(comCount=Count('comments'))\
        .order_by('-comCount')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
