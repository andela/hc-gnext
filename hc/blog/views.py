"""
Module with views to handle blog application CRUD functionalities.
"""

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

# local apps
from hc.blog.forms import CategoryForm, PostForm
from hc.blog.models import Category, Post
from hc.blog.mixins import CommonContentMixin, PostOwnerRequiredMixin

# third party apps
from braces.views import LoginRequiredMixin


class BlogIndexView(CommonContentMixin, generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    title = 'Blog Index'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        category_slug = self.request.GET.get('category', None)

        # filter posts by category
        if category_slug:
            posts = Post.objects.filter(categories__slug__contains=category_slug)
            return posts

        else:  # return default
            return Post._default_manager.all()

    def get_context_data(self, **kwargs):
        ctx = super(BlogIndexView, self).get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class CategoryCreateView(LoginRequiredMixin, CommonContentMixin, generic.CreateView):
    form_class = CategoryForm
    template_name = 'blog/post_form.html'
    title = 'Post Category'

    def get_context_data(self, **kwargs):
        ctx = super(CategoryCreateView, self).get_context_data(**kwargs)
        post_form = PostForm()
        categories = Category.objects.all()
        ctx['categories'] = categories
        ctx['post_form'] = post_form
        return ctx

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('hc-blog:post-create'))

    def get_success_url(self):
        messages.success(self.request, 'Blog post category created')
        return reverse('hc-blog:post-create')

    def form_invalid(self, form):
        messages.warning(self.request, 'There exists a category with that name')
        return HttpResponseRedirect(reverse('hc-blog:category-create'))


class BlogPostCreateView(LoginRequiredMixin, CommonContentMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'
    title = 'Create Blog'

    def get_success_url(self):
        messages.success(self.request, 'Blog post created')
        return reverse('hc-blog:index')

    def form_invalid(self, form):
        messages.warning(self.request, 'Please fix the errors below')
        return super(BlogPostCreateView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(BlogPostCreateView, self).get_form_kwargs()
        if 'create' not in kwargs:
            kwargs.update({'create': True})

        if 'request' not in kwargs:
            kwargs.update({'request': self.request})

        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(BlogPostCreateView, self).get_context_data(**kwargs)
        ctx['category_form'] = CategoryForm()
        return ctx


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
        messages.success(self.request, 'Post updated!')
        return reverse('hc-blog:post-detail', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self):
        """
        Add `request` object to form kwargs for further actions
        """

        kwargs = super(BlogPostUpdateView, self).get_form_kwargs()
        if 'update' not in kwargs:
            kwargs.update({'update': True})

        if 'request' not in kwargs:
            kwargs.update({'request': self.request})

        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(BlogPostUpdateView, self).get_context_data(**kwargs)
        ctx['page_action'] = 'update'
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
