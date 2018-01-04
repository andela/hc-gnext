"""
Registers models to Django admin site.
"""


from django.contrib import admin
from .models import Category, Post


class AdminCategory(admin.ModelAdmin):
    """
    Customize Category model in admin site.
    """

    list_display = ('id', 'name', 'timestamp', 'updated')
    list_filter = ('timestamp', )
    prepopulated_fields = ({'slug': ('name',)})
    search_fields = ('name', )


class AdminPost(admin.ModelAdmin):
    """
    Customize Post model in admin site.
    """

    list_display = ('id', 'title', 'timestamp', 'updated')
    list_filter = ('timestamp', 'categories')
    search_fields = ('title', )
    prepopulated_fields = ({'slug': ('title', )})


admin.site.register(Category, AdminCategory)
admin.site.register(Post, AdminPost)
