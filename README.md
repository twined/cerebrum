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


Color Scheme:
-------------
Default is:

#520E24;
#8F2041;
#DC554F;
#FF905E;
#FAC51C;
#FBA026;
#F87117;
#CF3510;
#890606;
#FF1B79;
#D6145F;
#AA0D43;
#7A0623;
#430202;
#500422;
#870B46;
#D0201A;
#FF641A;
