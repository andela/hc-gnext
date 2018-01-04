from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from .forms import CategoryForm, PostForm
from .models import Category, Post


class BlogIndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(BlogIndexView, self).get_context_data(**kwargs)
        ctx['posts'] = Post.objects.all()
        return ctx


class CreateCategoryView(CreateView):
    form_class = CategoryForm
    template_name = 'blog/category_create.html'

    def get_success_url(self):
        return reverse('hc-blog:category-create')

    def get_context_data(self, **kwargs):
        ctx = super(CreateCategoryView, self).get_context_data(**kwargs)
        post_form = PostForm()
        categories = Category.objects.all()
        ctx['categories'] = categories
        ctx['post_form'] = post_form
        ctx['page_action'] = 'create'
        return ctx


class CreateBlogPostView(CreateView):
    form_class = PostForm
    template_name = 'blog/category_create.html'

    def get_success_url(self):
        return reverse('hc-blog:index')

    def get(self, request, *args, **kwargs):
        super(CreateBlogPostView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('hc-blog:category-create'))

    def get_form_kwargs(self):
        kwargs = super(CreateBlogPostView, self).get_form_kwargs()
        if not hasattr(kwargs, 'request'):
            kwargs.update({'request': self.request})

        return kwargs


class RetrievePostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/category_create.html'

    def get_success_url(self):
        return reverse('hc-blog:post-detail', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self):
        kwargs = super(UpdatePostView, self).get_form_kwargs()
        if not hasattr(kwargs, 'request'):
            kwargs.update({'request': self.request})

        return kwargs

    def form_invalid(self, form):
        print(form)
        return super(UpdatePostView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(UpdatePostView, self).get_context_data(**kwargs)
        ctx['page_action'] = 'update'
        post_form = ctx.get('form', )
        ctx.update({'post_form': post_form})
        return ctx
