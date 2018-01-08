"""
Blog application url routes
"""

from django.conf.urls import url
from hc.blog import views

app_name = 'hc-blog'

urlpatterns = [
    url(r'^$', views.BlogIndexView.as_view(), name='index'),
    url(r'^category/create$',
        views.CategoryCreateView.as_view(),
        name='category-create'),

    url(r'^post/create$',
        views.BlogPostCreateView.as_view(),
        name='post-create'),

    url(r'^post/(?P<slug>[a-zA-Z0-9_-]+)$',
        views.BlogPostDetailView.as_view(),
        name='post-detail'),

    url(r'^post/(?P<slug>[a-zA-Z0-9_-]+)/edit/$',
        views.BlogPostUpdateView.as_view(),
        name='post-update'),

    url(r'^post/(?P<slug>[a-zA-Z0-9_-]+)/delete/$',
        views.BlogPostDeleteView.as_view(),
        name='post-delete'),
]
