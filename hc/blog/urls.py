from django.conf.urls import url
from hc.blog import views

app_name = 'hc-blog'

urlpatterns = [
    url(r'^category/create', views.CreateCategoryView.as_view(), name='category-create'),
]