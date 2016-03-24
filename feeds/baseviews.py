from django.views.generic import ListView


class PaginatedListView(ListView):
    """
    PaginatedListView
    =================

    Extends the generic ListView for features with a smarter pagination.

    .. todo:
      - Implement the actual smarter pagination
        See also:
        https://github.com/jamespacileo/django-pure-pagination/blob/master/pure_pagination/paginator.py
      - Allow custom user settings for logged in users
        from :py:modules:`feeds.options`
    """
    def get_paginate_by(self, queryset):
        if 'paginate_by' in self.request.GET:
            return int(getattr(self.request.GET, 'paginate_by', 10))
        # elif type(self.request.user) is not AnonymousUser:
        #    if 'number_initially_displayed' in self.request.user.options:
        #        return self.request.user.options.number_initially_displayed
        return 10
    pass
