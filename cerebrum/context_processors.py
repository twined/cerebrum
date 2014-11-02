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
    cfg = getattr(settings, 'ADMIN_CONFIG')
    return {
        'SHORT_TTL': cfg['SHORT_TTL'],
        'MEDIUM_TTL': cfg['MEDIUM_TTL'],
        'LONG_TTL': cfg['LONG_TTL'],
        'FOREVER_TTL': cfg['FOREVER_TTL'],
    }


def date_now(request):
    return {'date_now': datetime.datetime.now()}
