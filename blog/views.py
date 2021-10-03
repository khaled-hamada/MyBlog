from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity


from .models import Post, Comment
from .forms import  EmailPostForm, CommentPostForm,\
                    SearchForm


from taggit.models import Tag
class PostList(ListView):
    queryset = Post.publishedPosts.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug', None)
       
        if tag_slug :
            self.tag = get_object_or_404(Tag, slug =tag_slug )
            self.queryset = self.queryset.filter(tags__in = [self.tag])
        return self.queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        try :
            context['tag'] = self.tag 
        except :
           context['tag'] = None
        return context
    

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            slug = post,
                            status= 'published',
                            published__year = year,
                            published__month = month,
                            published__day = day,

    )
    #List of active comments 
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        # validate data 
        comment_form = CommentPostForm(request.POST)
        
        if comment_form.is_valid():
            # print(comment_form.cleaned_data)
            # print(request.POST)
            # create but do not save to the db
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            #save to the db 
            new_comment.save()
            comment_form = CommentPostForm()
    else:
        comment_form = CommentPostForm()
    # get similar posts to recommend to the user 
    # see how the query is converted to sql 
    # last 4 posts ordered by tags_count and published date
    similar_posts = Post.publishedPosts.similar_posts(post.id)[:4]
    # print(similar_post.query)                
    return render(request, 'blog/post/detail.html',
                 {
                    'post':post,
                    'comment_form':comment_form,
                    'new_comment':new_comment,
                     'comments':comments,
                     'similar_posts':similar_posts,
                 })



def post_share(request, post_id: int) :
    post = get_object_or_404(Post, id = post_id, status='published')
    send = False
    # 2 possible http actions  get or post
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        
        if form.is_valid():
            # cleaned data allways contains 
            # the valid data only 

            cd = form.cleaned_data
            #send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n'\
                      f'{cd["name"]}\'s comments: {cd["comments"]}'
            
            send_mail(subject, message,'omarahmed010052@gmail',[cd['receiver']])
            send = True

        # else if not valid 
        # return http response with form.errors

            
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{
                    'post':post,
                    'form':form,
                    'sent':send,
                    })



def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search = SearchVector('title', 'body')
            ).filter(search = query)
        
    return render(request,
                  'blog/post/search.html',
                  {'form':form,
                  'query': query,
                  'results':results,
                  }  
                    )


def post_search_3(request):
    """another way of searching using ranking and weighting  """
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
       
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight= 'A') +\
                            SearchVector('body', weight='B')
                        
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
               
                rank = SearchRank(search_vector, search_query)
            ).filter(rank__gte = .3).order_by('-rank')
    
        
    return render(request,
                  'blog/post/search.html',
                  {'form':form,
                  'query': query,
                  'results':results,
                  }  
                    )


def post_search_2(request):
    """another way of searching using ranking  """
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
       
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                search=search_vector,
                rank = SearchRank(search_vector, search_query)
            ).filter(search = search_query).order_by('-rank')
    
        
    return render(request,
                  'blog/post/search.html',
                  {'form':form,
                  'query': query,
                  'results':results,
                  }  
                    )

def post_search_4(request):
    """another way of searching using trigram similarty  """
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
       
        if form.is_valid():
            query = form.cleaned_data['query']
            # search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
    
        
    return render(request,
                  'blog/post/search.html',
                  {'form':form,
                  'query': query,
                  'results':results,
                  }  
                    )
