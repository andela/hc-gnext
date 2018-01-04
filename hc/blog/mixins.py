class CommonContentMixin(object):
    """
    Defines attributes that are common or needed by almost all views.
    """

    def get_context_data(self, **kwargs):
        ctx = super(CommonContentMixin, self).get_context_data(**kwargs)
        previous_url = self.request.META.get('HTTP_REFERER', None)
        if previous_url:
            ctx['previous_url'] = previous_url
        return ctx
