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
        page_url = context['request'].build_absolute_uri()
        parsed_uri = urlparse(page_url)
        image_url = '%s://%s%s' % (
            parsed_uri.scheme, parsed_uri.netloc, kwargs['image_url'])
        return {
            'class_names': kwargs['class_names'],
            'page_url': page_url,
            'image_url': image_url,
            'description': kwargs['description']
        }

register.tag(Pinterest)
