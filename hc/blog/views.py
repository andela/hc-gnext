from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import CategoryForm, PostForm
from .models import Category, Post
from .mixins import CommonContentMixin

from braces.views import UserPassesTestMixin, LoginRequiredMixin


class BlogIndexView(LoginRequiredMixin, CommonContentMixin, generic.TemplateView):
    template_name = 'blog/index.html'

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


class CreateCategoryView(LoginRequiredMixin, CommonContentMixin, generic.CreateView):
    form_class = CategoryForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Blog post category created')
        return reverse('hc-blog:category-create')

    def get_context_data(self, **kwargs):
        ctx = super(CreateCategoryView, self).get_context_data(**kwargs)
        post_form = PostForm()
        categories = Category.objects.all()
        ctx['categories'] = categories
        ctx['post_form'] = post_form
        ctx['page_action'] = 'create'
        return ctx


class CreateBlogPostView(LoginRequiredMixin, CommonContentMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Blog post created')
        return reverse('hc-blog:index')

    def get(self, request, *args, **kwargs):
        """
        Redirect all GET requests to the view
        """

        super(CreateBlogPostView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('hc-blog:category-create'))

    def get_form_kwargs(self):
        kwargs = super(CreateBlogPostView, self).get_form_kwargs()
        if 'request' not in kwargs:
            kwargs.update({'request': self.request})

        return kwargs


class RetrievePostDetailView(LoginRequiredMixin, CommonContentMixin, generic.DetailView):
    model = Post


class UpdatePostView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CommonContentMixin,
    generic.UpdateView):
    model = Post
    form_class = PostForm

    def test_func(self, user):
        slug = self.kwargs.get('slug', None)
        if slug:
            obj = Post.objects.filter(slug=slug)
            if obj.exists():
                owner = obj.first().created_by == user
                return owner if True else messages.warning(self.request, 'You are not the owner of the blog post!')
        return False

    def get_success_url(self):
        return reverse('hc-blog:post-detail', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self):
        kwargs = super(UpdatePostView, self).get_form_kwargs()
        if 'request' not in kwargs:
            kwargs.update({'request': self.request})

        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(UpdatePostView, self).get_context_data(**kwargs)
        ctx['page_action'] = 'update'
        ctx['category_form'] = CategoryForm()
        return ctx


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, CommonContentMixin, generic.DeleteView):
    model = Post

    def test_func(self, user):
        slug = self.kwargs.get('slug', None)
        if slug:
            obj = Post.objects.filter(slug=slug)
            if obj.exists():
                owner = obj.first().created_by == user
                return owner if True else messages.warning(self.request, 'You are not the owner of the blog post!')
        return False

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        confirm = post_data.get('confirm', False)

        if confirm != 'on' or not confirm:
            return HttpResponseRedirect(
                reverse('hc-blog:post-detail', kwargs={'slug': kwargs.get('slug', '')}))

        return super(DeletePostView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Blog post succesfully deleted')
        return reverse('hc-blog:index')