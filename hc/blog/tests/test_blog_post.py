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

        # blog post form.
        self.post_title = 'test title'
        self.blog_post_form = dict(
            categories=[self.category.id, ],
            title=self.post_title,
            content='this is a blog post test content')

        self.create_blog_post_link = reverse('hc-blog:post-create')

    def test_user_can_create_blog_post(self):
        """
        User should be able to create blog post content.
        """

        # create post content.
        response = self.client.post(self.create_blog_post_link, self.blog_post_form)

        # filter posts using title in blog_post_form.
        posts = Post.objects.filter(title=self.post_title)

        # assertions.
        self.assertEqual(response.status_code, 302)
        self.assertGreater(posts.count(), 0)
        self.assertEqual(posts.first().title, self.post_title)
        self.assertEqual(posts.first().categories.count(), 1)
        assert posts.first().categories.first() == self.category

    def test_user_can_view_blog_post(self):
        """
        A user should be able to view a single blog post entry.
        """

        self.client.post(self.create_blog_post_link, self.blog_post_form)
        post = Post.objects.get(name=self.blog_post_form.get('title'))
        blog_post_detail_url = reverse('hc-blog:blog-detail', kwargs={'slug': post.slug})

        view_response = self.client.get(blog_post_detail_url)

        view_context = view_response.context()

        assert view_response.status_code == 200
        self.assertIn(post, view_context)