"""
This module implements blog model classes.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Timestamp(models.Model):
    """
    Implements common fields used in all model classes.
    """

    class Meta:
        """
        Set model as abstract only.
        """

        abstract = True

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)


class Category(Timestamp):
    """
    Implements category model for post objects.
    """

    class Meta:
        """
        Set model meta attributes.
        """

        ordering = ('-id', )
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def get_absolute_url(self):
        """
        Generates url link for each post.

        :return: url
        """

    def __str__(self):
        return '%s' % self.name.capitalize()


class Post(Timestamp):
    """
    Implement actual post model for post objects.
    """

    class Meta:
        """
        Set model meta attributes.
        """

        ordering = ('-id', )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    category = models.ManyToManyField(Category, related_name='categories')
    content = models.TextField()

    def get_absolute_url(self):
        """
        Generates url link for each post.

        :return: url
        """

    def __str__(self):
        return '%s' % self.title.capitalize()