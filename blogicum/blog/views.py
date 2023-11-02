import datetime as dt
#from django.urls import reverse_lazy
#from blog.forms import CommentForm, PostForm, UserForm
from blog.models import Category, Post, User, Comment
from django.shortcuts import get_object_or_404, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

LAST_POSTS = 5


def core_filter(posts_object):
    filters = {
        'is_published': True,
        'category__is_published': True,
        'pub_date__date__lte': dt.datetime.today()
    }
    return posts_object.filter(**filters)


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        # Выполняем фильтрацию и сортировку данных, как в вашей функции
        return core_filter(Post.objects.all())[:LAST_POSTS]


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=self.kwargs.get(
            'username'
        ))
        return context


class ProfileUpdateView(UpdateView):
    #model = User
    #form_class = UserForm
    #template_name = 'blog/user.html'
    #success_url = reverse_lazy('blog:index')
    pass


class PostCreateView(CreateView):
    pass


class PostEditView(CreateView):
    pass


class PostDeleteView(DeleteView):
    pass


class PostUpdateView(UpdateView):
    pass


class CommentUpdateView(UpdateView):
    pass


class CommentDeleteView(DeleteView):
    pass


def post_detail(request, post_id):
    return render(request, 'blog/detail.html', {
        'post': get_object_or_404(
            core_filter(Post.objects.all()), id=post_id),
    })


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'  # Указываем имя шаблона
    context_object_name = 'post_list'  # Указываем имя переменной в контексте

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug, is_published=True)
        return core_filter(category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context


def add_comment():
    pass
