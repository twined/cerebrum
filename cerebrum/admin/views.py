# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Main admin view for the Cerebrum app
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import View

from ..mixins import LoginRequiredMixin
from ..cache import cache_delete_pattern
from .. import registry


class DashboardIndex(LoginRequiredMixin, TemplateView):
    """
    Presents the admin dashboard.
    """
    template_name = 'dashboard/admin/index.html'

    def get_context_data(self, **kwargs):
        '''
        build dashboard plugins
        '''
        context = super(DashboardIndex, self).get_context_data(**kwargs)
        context['plugins'] = [registry.registry[key]()
                              for key, val in registry.registry.items()]
        return context


class CacheBustView(LoginRequiredMixin, View):
    """
    Bust that cache, baby!
    """

    def get(self, request, *args, **kwargs):
        # deletes all template fragment caches
        cache_delete_pattern('template.cache.*')
        messages.success(
            self.request,
            'Cachen er slettet!',
            extra_tags='msg'
        )
        return HttpResponseRedirect(reverse('admin:dashboard'))
