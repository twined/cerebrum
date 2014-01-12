from django.core.urlresolvers import reverse_lazy

APP_ADMIN_MENU = {
    'Administrasjon': {
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
    }
}
