from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone as tz
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import CommentForm, PostForm, UserForm
from blog.models import Category, Post, User
from blog.mixin import (CommentMixin, IsEditMixin,
                        IsDeleteMixin, DispatchMixin,
                        AggregateQuerysetMixin
                        )
from core.const import TEN_PUB


@login_required
def add_comment(request, post_id):
    comment = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        commentary = form.save(commit=False)
        commentary.author = request.user
        commentary.post = comment
        commentary.save()
    return redirect('blog:post_detail', post_id=post_id)


class IndexListView(ListView, AggregateQuerysetMixin):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = TEN_PUB

    def get_queryset(self):
        queryset = Post.objects.select_related('author'
                                               ).prefetch_related('comments')
        queryset = self.get_filter_queryset(queryset)
        queryset = self.aggregate_queryset(queryset)
        return queryset

    def get_filter_queryset(self, queryset):
        queryset = queryset.filter(
            pub_date__lt=tz.now(),
            is_published=True,
            category__is_published=True,
        )
        return queryset


class ProfileListView(ListView, AggregateQuerysetMixin):
    model = Post
    template_name = 'blog/profile.html'
    ordering = 'id'
    paginate_by = TEN_PUB

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=self.kwargs.get(
            'username'
        ))
        return context

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = author.posts.all()
        queryset = self.aggregate_queryset(queryset)
        return queryset


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    paginate_by = TEN_PUB

    def get_filtered_queryset(self):
        queryset = self.object.comments.select_related('author').filter(
            post_id__is_published=True,
            post_id__category__is_published=True,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'),)

        is_author = post.author == self.request.user
        is_published = post.is_published and post.category.is_published
        is_published_in_time = post.pub_date <= tz.now()

        if not (is_author or (is_published and is_published_in_time)):
            raise Http404('Page does not exist')

        context['comments'] = self.get_filtered_queryset()
        context['form'] = CommentForm()
        return context


class CategoryListView(ListView, AggregateQuerysetMixin):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = TEN_PUB

    def get_queryset(self):
        queryset = self.get_filter_queryset()
        queryset = self.aggregate_queryset(queryset)
        return queryset

    def get_filter_queryset(self):
        category = self.get_category()
        queryset = category.posts.filter(
            pub_date__lt=tz.now(),
            is_published=True,
        )
        return queryset

    def get_category(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return category


class PostUpdateView(DispatchMixin, LoginRequiredMixin,
                     UpdateView, IsEditMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    posts = None

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get('post_id')}
        )


class PostDeleteView(DispatchMixin, LoginRequiredMixin,
                     DeleteView, IsDeleteMixin):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'


class CommentUpdateView(LoginRequiredMixin, CommentMixin,
                        UpdateView, IsEditMixin):
    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin,
                        DeleteView, IsDeleteMixin):
    pass
