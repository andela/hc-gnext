from django.core.urlresolvers import reverse
from hc.test import BaseTestCase
from hc.blog.models import Category, Post


class BlogPostTestCase(BaseTestCase):
    def setUp(self):
        """
        Override setUp method and add blog post test data
        """
        super(BlogPostTestCase, self).setUp()
        password = 'password'
        login_link = reverse('hc-login')
        login_form = dict(email=self.alice.email, password=password)

        # login alice
        self.client.post(login_link, login_form)

        # create category.
        category = Category()
        category.name = 'test category'
        category.slug = 'test-category'
        category.save()
        self.category = category

        self.create_blog_post_link = reverse('hc-blog:create-post')

    def test_user_can_create_blog_post(self):
        """
        User should be able to create blog post content.
        """

        # blog post form.
        post_title = 'test title'
        blog_post_form = dict(
            categories=[self.category.id, ],
            title=post_title,
            content='this is a blog post test content')

        # create post content.
        response = self.client.post(self.create_blog_post_link, blog_post_form)

        # filter posts using title in blog_post_form.
        posts = Post.objects.filter(title=post_title)

        # assertions.
        self.assertEqual(response.status_code, 302)
        self.assertGreater(posts, 0)
        self.assertIs(posts.first().title, post_title)

