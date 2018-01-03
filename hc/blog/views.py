from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView
from .forms import CategoryForm
from .models import Category


class BlogIndexView(TemplateView):
    template_name = 'blog/blog_index.html'


class CreateCategoryView(CreateView):
    form_class = CategoryForm
    template_name = 'blog/category_create.html'

    def get_success_url(self):
        return reverse('hc-blog:category-create')

    def get_context_data(self, **kwargs):
        ctx = super(CreateCategoryView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        ctx['categories'] = categories
        return ctx

