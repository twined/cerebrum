# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Context processors for the Cerebrum app
# Provides {{ admin }} dictionary in all templates.
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

import datetime

from django.core.exceptions import ImproperlyConfigured
from cerebrum import settings


def admin(request):
    try:
        cfg = getattr(settings, 'ADMIN_CONFIG')
    except AttributeError:
        raise ImproperlyConfigured(
            "'ADMIN_CONFIG' must be set in settings.py."
        )

    return {'admin': cfg}


def cache_constants(request):
    return {
        'SHORT_TTL': 60*10,
        'MEDIUM_TTL': 60*30,
        'LONG_TTL': 60*60,
        'FOREVER_TTL': 60*60*24*7
    }


def date_now(request):
    return {'date_now': datetime.datetime.now()}
