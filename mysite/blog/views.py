from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNoExist:
#         raise Http404('No Post Found.')
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})
def post_detail(request, id):
    post = get_object_or_404(Post,id = id, status = Post.Status.PUBLISHED)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})

# Create your views here.
