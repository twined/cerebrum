# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Admin tags for the Cerebrum app
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

from collections import OrderedDict

from django import template
from django.conf import settings

from cerebrum.utils import merge_settings

register = template.Library()


@register.inclusion_tag(
    'admin/templatetags/display_menu.html',
    takes_context=True)
def display_menu(context):
    merged_menu = OrderedDict({})
    for app in settings.INSTALLED_APPS:
        admin_menu_dotpath = '%s.admin.config' % app
        try:
            # try to load app.admin.config
            module = __import__(admin_menu_dotpath, fromlist=[None])
            menu = getattr(module, 'APP_ADMIN_MENU')
            merged_menu = merge_settings(merged_menu, menu)
        except ImportError:
            pass
        except AttributeError:
            pass

    # sort the dict
    for key, menu_subitem in merged_menu.items():
        merged_menu[key] = OrderedDict(
            sorted(
                menu_subitem.items(),
                key=lambda item: item[1]['order']
            )
        )
    merged_menu = OrderedDict(sorted(merged_menu.items(), key=lambda t: t[0]))

    return {
        'menu': merged_menu,
        'request': context['request'],
    }
