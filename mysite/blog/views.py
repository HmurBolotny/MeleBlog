#from calendar import month

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm
from django.views.decorators.http import  require_POST
from django.http import Http404

class PostListView(ListView):
    '''alternativ views list_list'''
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by =  3
    template_name = 'blog/post/list.html'

# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNoExist:
#         raise Http404('No Post Found.')
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments':comments,
                   'form':form})


def post_list(request):
    post_list = Post.published.all()
    #разбивка постраничная
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id =post_id, status= Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post':post,'form':form,'comment':comment})
# Create your views here.