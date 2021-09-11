from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import  EmailPostForm, CommentPostForm

class PostList(ListView):
    queryset = Post.publishedPosts.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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
            # create but do not save to the db
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            #save to the db 
            new_comment.save()
            comment_form = CommentPostForm()
    else:
        comment_form = CommentPostForm()
    
    return render(request, 'blog/post/detail.html',
                 {
                    'post':post,
                    'comment_form':comment_form,
                    'new_comment':new_comment,
                     'comments':comments
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
