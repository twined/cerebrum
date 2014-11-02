from django.conf import settings

ADMIN_CONFIG = {
    'SHORT_TTL': 60*60*2,
    'MEDIUM_TTL': 60*60*6,
    'LONG_TTL': 60*60*14,
    'FOREVER_TTL': 60*60*24*7,
    'site_url': '',
    'site_version': '1.0',
    'site_name': 'NAME',
    'menu_colors': [
        '#FBA026;',
        '#F87117;',
        '#CF3510;',
        '#890606;',
        '#FF1B79;',

        '#520E24;',
        '#8F2041;',
        '#DC554F;',
        '#FF905E;',
        '#FAC51C;',

        '#D6145F;',
        '#AA0D43;',
        '#7A0623;',
        '#430202;',
        '#500422;',

        '#870B46;',
        '#D0201A;',
        '#FF641A;',
    ]
}

ADMIN_CONFIG.update(getattr(settings, 'ADMIN_CONFIG', {}))
