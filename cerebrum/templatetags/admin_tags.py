# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Admin tags for the Cerebrum app
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

from collections import OrderedDict

from django import template
from django.conf import settings

from cerebrum.utils import merge_settings
from cerebrum.settings import ADMIN_CONFIG

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
    #import ipdb; ipdb.set_trace()
    for key, menu_subitem in merged_menu.items():
        merged_menu[key]['menu'] = OrderedDict(
            sorted(
                menu_subitem['menu'].items()
                if 'menu' in menu_subitem else menu_subitem.items(),
                key=lambda item: item[1]['order']
            )
        )
        merged_menu[key]['config'] = {
            #'bgcolor': menu_subitem['bgcolor']
            #if 'bgcolor' in menu_subitem else '#333333',
            'icon': menu_subitem['icon']
            if 'icon' in menu_subitem else 'fa fa-columns icon',
            'anchor': menu_subitem['anchor']
            if 'anchor' in menu_subitem else 'anchor'
        }
    merged_menu = OrderedDict(sorted(merged_menu.items(), key=lambda t: t[0]))
    i = 0
    colors = ADMIN_CONFIG['menu_colors']
    for k, v in merged_menu.items():
        v['bgcolor'] = colors[i]
        i += 1

    return {
        'menu': merged_menu,
        'request': context['request'],
    }
