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

        # create post object.
        self.post_title = 'test title'
        post = Post()
        post.title = 'test post'
        post.slug = 'test-post'
        post.content = 'test post content'
        post.created_by = self.alice
        post.save()
        post.categories.add(category)
        self.post = post

        # blog post form.
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
        post = Post.objects.get(title=self.post_title)
        blog_post_detail_url = reverse('hc-blog:post-detail', kwargs={'slug': post.slug})

        view_response = self.client.get(blog_post_detail_url)

        view_context = view_response.context

        # detail view contains object in the context which is an instance of Post model.
        obj = [item.get('object') for item in view_context[0]][0]

        self.assertEqual(view_response.status_code, 200)
        self.assertEqual(post, obj)

    def test_user_can_update_blog_post(self):
        """
        A user should be able to update created blog posts.
        """

        # new category
        new_category = Category()
        new_category.name = 'new category'
        new_category.slug = 'new-category'
        new_category.save()

        # new title
        new_title = 'new title'

        update_post_link = reverse('hc-blog:post-update', kwargs={'slug': self.post.slug})

        # update title and add extra category
        update_form = dict(
            title=new_title,
            categories=[self.category.id, new_category.id, ],
            content=self.post.content)

        # assert category is 1 initially
        self.assertEqual(Post.objects.count(), 1)

        update_response = self.client.post(update_post_link, update_form)

        # query posts
        posts = Post.objects.all()

        # assertions
        self.assertEqual(update_response.status_code, 302)
        self.assertTrue(posts.count(), 1)
        self.assertEqual(posts.first().categories.count(), 2)
        self.assertTrue(posts.filter(title=new_title).exists())

    def test_user_can_delete_post(self):
        """

        :return:
        """
        delete_form = dict(confirm='on')
        delete_post_link = reverse('hc-blog:post-delete', kwargs={'slug': self.post.slug})
        delete_response = self.client.post(delete_post_link, delete_form)

        self.assertEqual(delete_response.status_code, 302)
        with self.assertRaises(self.post.DoesNotExist):
            Post.objects.get(title=self.post.title)


