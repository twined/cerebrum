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
