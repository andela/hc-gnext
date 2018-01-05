"""
Module with custom mixin classes to avoid code repetition.
"""

from django.contrib import messages
from .models import Post
from braces.views import UserPassesTestMixin


class CommonContentMixin(object):
    """
    Defines attributes that are common or needed by almost all views.
    """

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'title'):
            setattr(self, 'title', '')

        return super(CommonContentMixin, self).dispatch(request, *args, **kwargs)

    def set_title(self, title):
        print(title, self.title)
        return setattr(self, title, title)

    def get_context_data(self, **kwargs):
        ctx = super(CommonContentMixin, self).get_context_data(**kwargs)

        previous_url = self.request.META.get('HTTP_REFERER', None)
        if previous_url:
            ctx['previous_url'] = previous_url

        ctx['title'] = getattr(self, 'title')
        return ctx


class PostOwnerRequiredMixin(UserPassesTestMixin):
    """
    Handle views that require users to be the owners of the blog post objects.

    Users who require to perform delete and update actions must pass the test method below.
    """

    def test_func(self, user):
        """
        Define rules that user must pass

        :param user: logged in user
        :return: bool
        """
        slug = self.kwargs.get('slug', None)
        if slug:
            obj = Post.objects.filter(slug=slug)

            if obj.exists():
                owner = obj.first().created_by == user

                if not owner:
                    messages.warning(self.request, 'You are not the owner of the blog post!')

                return owner

        return False
