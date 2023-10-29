import datetime as dt

from blog.models import Category, Post
from django.shortcuts import get_object_or_404, render

LAST_POSTS = 5


def core_filter(posts_object):
    filters = {
        'is_published': True,
        'category__is_published': True,
        'pub_date__date__lte': dt.datetime.today()
    }
    return posts_object.filter(**filters)


def index(request):
    return render(request, 'blog/index.html', {
        'post_list': core_filter(Post.objects.all())[:LAST_POSTS],
    })


def post_detail(request, post_id):
    return render(request, 'blog/detail.html', {
        'post': get_object_or_404(
            core_filter(Post.objects.all()), id=post_id),
    })


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = core_filter(category.posts)

    return render(request, 'blog/category.html', context={
        'post_list': post_list,
        'category': category,
    })
