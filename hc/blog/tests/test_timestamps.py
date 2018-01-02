"""
Tests model timestamps fields to assert category and post objects are stored correctly.
"""


from django.contrib.auth.models import User
from django.test import TestCase
from hc.blog.models import Category, Post


class TestTimestampsCase(TestCase):
    """
    Test timestamp and updated fields.
    """

    def setUp(self):
        user = User.objects.create_user(
            'test_user',
            'test_user@email.com',
            'test_userpassword')

        # create and save Category instance.
        category = Category()
        category.name = 'Test category'
        category.save()

        # create and save Post instance.
        post = Post()
        post.title = 'Test post'
        post.content = 'Test post content'
        post.created_by = user
        post.save()

        # add category after thr post instance has been saved.
        post.category.add(category)

        self.user = user
        self.category = category
        self.post = post

    def test_category_updated_value_should_be_recent_than_created_at_value(self):
        """
        updated field value should be greater than timestamp value when the object is modified.
        """

        # save the category object instance.
        self.category.save()
        self.assertGreater(self.category.updated, self.category.timestamp)

    def test_post_updated_value_should_be_recent_than_created_at_value(self):
        """
        updated field value should be greater than timestamp value when the object is modified.
        """

        # save the post object instance.
        self.post.save()
        self.assertGreater(self.post.updated, self.post.timestamp)