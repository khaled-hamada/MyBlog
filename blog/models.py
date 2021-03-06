from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    """ custom post manager to filter data by status """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

    def searchBody(self, *args, **kwargs):
        pass

    def similar_posts(self, post_id):
        post = self.get_queryset().get(id = post_id)
        tags_list = post.tags.values_list('id', flat=True)
        similar_posts = self.get_queryset().filter(tags__in=tags_list).\
            exclude(id=post.id)
        similar_posts = similar_posts.annotate(tags_count = models.Count('tags')).\
             order_by('-tags_count', '-published')

        return similar_posts

class Postable(models.Model):
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(Postable):
    """  A post model class to create blog posts """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    objects = models.Manager()  # The default manager.
    publishedPosts = PublishedManager()  # Our custom manager.
    
    title = models.CharField(max_length=264)
    slug = models.SlugField(max_length=264, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE ,
                                related_name='blog_posts')
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length = 16,
                              choices=STATUS_CHOICES,
                              default = 'draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                        args = [
                            self.published.year,
                            self.published.month,
                            self.published.day,
                            self.slug
                        ]
        )
                           
    
class Comment(Postable):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name= 'comments')
    name = models.CharField(max_length=254)
    email = models.EmailField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comment by{self.name} on {self.post} '
    
