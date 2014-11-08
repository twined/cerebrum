# -*- coding: utf-8 -*-
"""
// Twined - Cerebrum
// admin url definitions for the Cerebrum app
// (c) Twined/Univers 2009-2014. All rights reserved.
"""

from django.conf.urls import patterns, url, include
from django.conf import settings
from cerebrum.admin.views import DashboardIndex, CacheBustView

urlpatterns = patterns(
    'admin',
    url(r'^$', DashboardIndex.as_view(), {}, name="dashboard"),
    url(r'^cachebust/$', CacheBustView.as_view(), {}, name="cachebust"),
)

urlpatterns += patterns(
    '',
    url(r'^login/', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/', 'django.contrib.auth.views.logout', name="logout"),
)

# grab urls and configs from INSTALLED_APPS
for app in settings.INSTALLED_APPS:
    admin_cfg_dotpath = '%s.admin.config' % app
    admin_urls_dotpath = '%s.admin.urls' % app
    try:
        module = __import__(admin_cfg_dotpath, fromlist=[None])
        urlcfg = getattr(module, 'APP_ADMIN_URLS', '')
        if not urlcfg:
            continue
        urlpatterns += patterns(
            'admin',
            url(
                r'^%s/' % urlcfg['url_base'],
                include(
                    admin_urls_dotpath,
                    namespace=urlcfg['namespace'],
                )
            )
        )
    except ImportError, e:
        # we don't catch the ImportErrors that looks for admin
        # files, since they're not in every app
        #  import ipdb; ipdb.set_trace()
        if str(e) in ('No module named config',
                      'No module named admin.config'):
            pass
            #  if settings.DEBUG:
            #    print("%s -> %s" % (admin_cfg_dotpath, str(e)))
            #  else:
            #    pass
        else:
            print "app failing: %s" % app
            raise ImportError(e)
