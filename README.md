CEREBRUM
========

**NOTE: This is tailored for the twined project structure,
it probably won't work too well without customization on other
project bootstraps.**

Installation:
-------------

    pip install -e git://github.com/twined/cerebrum.git#egg=cerebrum-dev


Usage:
------

Add `cerebrum` to `INSTALLED_APPS` and add this to your urlpatterns:

    # admin urls
    url(
        r'^admin/', include('cerebrum.admin.admin_urls', namespace="admin")
    ),

Then add this to your `settings.py`

    TEMPLATE_CONTEXT_PROCESSORS += (
        'cerebrum.context_processors.admin',
    )

    ADMIN_CONFIG = {
        'site_name': 'SITENAME',
        'site_url': 'DOMAIN.COM',
    }

    from django.core.urlresolvers import reverse_lazy
    LOGIN_REDIRECT_URL = reverse_lazy('admin:dashboard')
    LOGIN_URL = '/admin/login/'
    LOGOUT_URL = '/admin/logout/'

Templatetags
------------

*Social buttons*

    {% load social_buttons %}
    {% pinterest image=post.featured_image.url description=post.header class_names='icon-pinterest' %}

*Cache*

    {% load cache_tags %}
    {% cache MEDIUM_TTL fragment_name obj.pk [var2] .. %}
        .. some expensive processing ..
    {% endcache %}


Admin config
------------
Default is:

    ADMIN_CONFIG = {

        # Cache constants. Use these in your templates when utilizing
        # {% load cache_tags %}

        'SHORT_TTL': 60*60*2,
        'MEDIUM_TTL': 60*60*6,
        'LONG_TTL': 60*60*14,
        'FOREVER_TTL': 60*60*24*7,

        # Site constants

        'site_url': '',
        'site_version': '1.0',
        'site_name': 'NAME',

        # Menu color cycle for admin apps

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
