# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Main admin view for the Cerebrum app
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View

from ..views import LoginRequiredMixin


class DashboardIndex(LoginRequiredMixin, TemplateView):
    """
    Presents the admin dashboard.
    """
    template_name = 'dashboard/admin/index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardIndex, self).get_context_data(**kwargs)
        return context


class CacheBustView(LoginRequiredMixin, View):
    """
    Bust that cache, baby!
    """

    def get(self, request, *args, **kwargs):
        cache.delete_pattern('*')
        messages.success(
            self.request,
            'Cachen er slettet!',
            extra_tags='msg'
        )
        return HttpResponseRedirect(reverse('admin:dashboard'))
