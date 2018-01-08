"""
Test module for post category CRUD functionality
"""


from django.core.urlresolvers import reverse
from hc.test import BaseTestCase
from hc.blog.models import Category


class TestPostCategoryCase(BaseTestCase):
    def setUp(self):
        super(TestPostCategoryCase, self).setUp()
        self.login_url = reverse('hc-login')
        self.login_form = dict(email=self.alice.email, password='password')

        # create post url
        self.create_category_url = reverse('hc-blog:category-create')
        self.category_form = dict(name='test category')

    def test_can_create_post_category(self):
        # login user
        self.client.post(self.login_url, self.login_form, follow=True)

        # create post category
        res = self.client.post(self.create_category_url, self.category_form, follow=True)

        category_name = self.category_form.get('name', '')

        # query from db
        obj = Category.objects.get(name=category_name)

        # assertions
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, category_name)
