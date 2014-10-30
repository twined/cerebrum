"""Custom Django template tag for caching"""
from __future__ import unicode_literals
import hashlib
import logging
from random import randint

from django.conf import settings
from django.template import (Library, Node, TemplateSyntaxError,
                             VariableDoesNotExist, Variable)
from django.core.cache import get_cache, cache
from django.utils.http import urlquote
from django.utils.encoding import force_bytes

logger = logging.getLogger(__name__)

register = Library()

TEMPLATE_FRAGMENT_KEY_TEMPLATE = 'template.cache.%s.%s'
BUST_GET_PARAM = 'flush-the-cache'


def get_backend():
    """
    Returns the actual django cache object johnny is configured to use.
    This relies on the settings only;  the actual active cache can
    theoretically be changed at runtime.
    """
    enabled = [n for n, c in sorted(settings.CACHES.items())
               if c.get('TEMPLATETAG_CACHE', False)]
    if len(enabled) > 1:
        logger.warn("Multiple caches configured for the HTML fragment cache; "
                    "using %s.", enabled[0])
    if enabled:
        return get_cache(enabled[0])
    return cache

TEMPLATE_CACHE = get_backend()


def make_template_fragment_key(fragment_name, vary_on=None):
    """Create a safe and consistent cache key"""
    if vary_on is None:
        vary_on = ()
    else:
        vary_on += (settings.SITE_ID,)
    if fragment_name.endswith('|'):
        # get the first vary_on entry and add it to the fragment name.
        # this is for easier invalidation of the cache fragment
        fragment_name = '%s%s' % (fragment_name, vary_on[0])
    logger.debug(u"html fragment name: %s -- %s", fragment_name, vary_on)
    key = ':'.join(urlquote(var) for var in vary_on)
    args = hashlib.md5(force_bytes(key))
    return TEMPLATE_FRAGMENT_KEY_TEMPLATE % (fragment_name, args.hexdigest())


def _apply_jitter(num, variance=0.2):
    """Applies jitter within variance to num"""
    min_num = num * (1 - variance)
    max_num = num * (1 + variance)
    return randint(min_num, max_num)


class CacheNode(Node):
    bust_param = BUST_GET_PARAM

    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on):
        self.nodelist = nodelist
        self.expire_time_var = expire_time_var
        self.fragment_name = fragment_name
        self.vary_on = vary_on
        self.request = Variable('request')

    def needs_cache_busting(self, request):
        """
        Determine if we need to bust the cache based on query string
        """
        bust = False
        if request.GET and (self.bust_param in request.GET):
            bust = True
        return bust

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"cache" tag got an unknown variable: %r'
                                      % self.expire_time_var.var)
        # Randomized the TTL to avoid massive invalidation
        try:
            expire_time = _apply_jitter(int(expire_time))
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"cache" tag got a non-integer timeout '
                                      'value: %r' % expire_time)
        vary_on = [var.resolve(context) for var in self.vary_on]
        try:
            request = self.request.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"cache" tag cannot resolve request')

        cache_key = make_template_fragment_key(self.fragment_name, vary_on)
        value = TEMPLATE_CACHE.get(cache_key)
        if self.needs_cache_busting(request) or value is None:
            value = self.nodelist.render(context)
            TEMPLATE_CACHE.set(cache_key, value, expire_time)
        return value


@register.tag('cache')
def do_cache(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time +/- 20%.

    Usage::

        {% load cache %}
        {% cache [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endcache %}

    This tag also supports varying by a list of arguments::

        {% load cache %}
        {% cache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endcache %}

    Each unique set of arguments will result in a unique cache entry.
    Appending ?{0} to the request will re generate the cache entry
    """
    nodelist = parser.parse(('endcache',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError("'%r' tag requires at least 2 arguments."
                                  % tokens[0])
    return CacheNode(
        nodelist,
        parser.compile_filter(tokens[1]),
        tokens[2],  # fragment_name can't be a variable.
        [parser.compile_filter(token) for token in tokens[3:]])
