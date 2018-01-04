from django.conf.urls import url
from hc.blog import views

app_name = 'hc-blog'

urlpatterns = [
    url(r'^$', views.BlogIndexView.as_view(), name='index'),
    url(r'^category/create', views.CreateCategoryView.as_view(), name='category-create'),
    url(r'^post/create', views.CreateBlogPostView.as_view(), name='post-create'),

]