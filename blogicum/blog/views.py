import datetime as dt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from blog.forms import CommentForm, PostForm, UserForm
from blog.models import Category, Post, User, Comment
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

LAST_POSTS = 5


@login_required
def add_comment(request, pk):
    comment = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.birthday = comment
        comment.save()
    return redirect('blog:post_detail', pk=pk)


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
        return core_filter(Post.objects.all())


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
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    ordering = ('-pub_date',)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('post')
        )
        return context


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug, is_published=True)
        return core_filter(category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context
