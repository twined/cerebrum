from urlparse import urlparse

from django import template

from classytags.core import Options
from classytags.arguments import MultiKeywordArgument
from classytags.helpers import InclusionTag

register = template.Library()


class Pinterest(InclusionTag):
    '''
    {% pinterest image=post.featured_image.url description=post.header class_names='icon-pinterest' %}
    '''
    options = Options(
        MultiKeywordArgument('kwargs'),
    )

    template = 'templatetags/pinterest.html'

    def get_context(self, context, kwargs):
        '''

        '''
        has_http = False
        if kwargs['image_url'][0:7].lower() == 'http://':
            has_http = True

        page_url = context['request'].build_absolute_uri()
        parsed_uri = urlparse(page_url)
        if has_http:
            image_url = kwargs['image_url']
        else:
            image_url = '%s://%s%s' % (
                parsed_uri.scheme, parsed_uri.netloc, kwargs['image_url'])

        return {
            'class_names': kwargs['class_names'],
            'page_url': page_url,
            'image_url': image_url,
            'description': kwargs['description']
        }

register.tag(Pinterest)
