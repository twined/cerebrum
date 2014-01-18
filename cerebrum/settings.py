from django.conf import settings

CEREBRUM_SETTINGS = {
    'debug_admin_urls_autodiscovery': False,
}

CEREBRUM_SETTINGS.update(getattr(settings, 'CEREBRUM_SETTINGS', {}))
