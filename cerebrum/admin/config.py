from django.core.urlresolvers import reverse_lazy

APP_ADMIN_MENU = {
    'Admin': {
        'anchor': 'admin',
        'bgcolor': '#FB6B5B',
        'icon': 'fa fa-dashboard icon',

        'menu': {
            'Hjem': {
                'url': reverse_lazy('admin:dashboard'),
                'icon': 'icon-home',
                'order': 0,
            },
            'Slett cache': {
                'url': reverse_lazy('admin:cachebust'),
                'icon': 'icon-trash',
                'order': 0,
            },
            'Logg ut': {
                'url': reverse_lazy('admin:logout'),
                'icon': 'icon-home',
                'order': 0,
            },
        }
    }
}
