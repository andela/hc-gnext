"""
Module with views to handle blog application CRUD functionalities.
"""

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

# third party app
from braces.views import LoginRequiredMixin

from .forms import CategoryForm, PostForm
from .models import Category, Post
from .mixins import CommonContentMixin, PostOwnerRequiredMixin


class BlogIndexView(CommonContentMixin, generic.TemplateView):
    template_name = 'blog/index.html'
    title = 'Blog Index'

    def get_context_data(self, **kwargs):
        ctx = super(BlogIndexView, self).get_context_data(**kwargs)
        category_slug = self.request.GET.get('category', None)
        posts = Post.objects.all()

        # filter posts by category
        if category_slug:
            posts = Post.objects.filter(categories__slug__contains=category_slug)

        ctx['categories'] = Category.objects.all()
        ctx['posts'] = posts

        return ctx


class CategoryCreateView(LoginRequiredMixin, CommonContentMixin, generic.CreateView):
    form_class = CategoryForm
    template_name = 'blog/post_form.html'
    title = 'Post Category'

    def get_success_url(self):
        messages.success(self.request, 'Blog post category created')
        return reverse('hc-blog:category-create')

    def get_context_data(self, **kwargs):
        ctx = super(CategoryCreateView, self).get_context_data(**kwargs)
        post_form = PostForm()
        categories = Category.objects.all()
        ctx['categories'] = categories
        ctx['post_form'] = post_form
        ctx['page_action'] = 'create'
        return ctx


class BlogPostCreateView(LoginRequiredMixin, CommonContentMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'
    title = 'Create Blog'

    def get_success_url(self):
        messages.success(self.request, 'Blog post created')
        return reverse('hc-blog:index')

    def get(self, request, *args, **kwargs):
        """
        Redirect all GET requests to the view
        """

        super(BlogPostCreateView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('hc-blog:category-create'),)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('hc-blog:category-create'))

    def get_form_kwargs(self):
        kwargs = super(BlogPostCreateView, self).get_form_kwargs()
        if 'request' not in kwargs:
            kwargs.update({'request': self.request})

        return kwargs


class BlogPostDetailView(CommonContentMixin, generic.DetailView):
    model = Post
    title = 'Post'


class BlogPostUpdateView\
            (LoginRequiredMixin, PostOwnerRequiredMixin,
             CommonContentMixin, generic.UpdateView):

    model = Post
    form_class = PostForm
    title = 'Blog Update'

    def get_success_url(self):
        return reverse('hc-blog:post-detail', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self):
        """
        Add `request` object to form kwargs for further actions
        """

        kwargs = super(BlogPostUpdateView, self).get_form_kwargs()
        if 'request' not in kwargs:
            kwargs.update({'request': self.request})

        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(BlogPostUpdateView, self).get_context_data(**kwargs)
        ctx['page_action'] = 'update'
        ctx['category_form'] = CategoryForm()
        return ctx


class BlogPostDeleteView\
            (LoginRequiredMixin, PostOwnerRequiredMixin,
             CommonContentMixin, generic.DeleteView):

    model = Post
    title = 'Confirm delete'

    def post(self, request, *args, **kwargs):
        """
        Ensure users confirm they really want the post gone
        """

        post_data = request.POST
        confirm = post_data.get('confirm', False)

        if confirm != 'on' or not confirm:
            return HttpResponseRedirect(
                reverse('hc-blog:post-detail', kwargs={'slug': kwargs.get('slug', '')}))

        return super(BlogPostDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Blog post successfully deleted')
        return reverse('hc-blog:index')
