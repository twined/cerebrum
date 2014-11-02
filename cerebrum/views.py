# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Generic Views and Mixins for the Application app
# (c) Twined/Univers 2009-2013. All rights reserved.
# ----------------------------------------------------------------------


from django.views.generic import TemplateView, View
from django.utils.datastructures import MultiValueDictKeyError

from taggit.models import Tag

from .mixins import LoginRequiredMixin
from .utils import json_response


class TextTemplateView(TemplateView):
    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/plain'
        return super(TemplateView, self).render_to_response(
            context, **response_kwargs)


class BaseAJAXCheckSlugView(LoginRequiredMixin, View):
    """
    Checks given slug against the database
    """
    model = object

    def get(self, request, *args, **kwargs):
        if 'slug' not in request.GET:
            # slug wasn't passed.
            return json_response({
                'status': 400,
                'error_msg': 'No slug passed to pages::checkslug'
            })

        slug = request.GET['slug'].lower()

        if 'pk' in self.kwargs:
            # it's an edit. it's ok if it's the same as before
            obj = self.model.objects.get(pk=self.kwargs['pk'])
            if obj.slug == slug:
                return json_response({
                    'status': 200,
                    'slug': slug,
                })

        index = 1
        orginal_slug = slug
        while True:
            if self.model.objects.filter(slug=slug).count() == 0:
                return json_response({
                    'status': 200,
                    'slug': slug
                })
            # the slug exists, iterate through until we find a free one
            index += 1
            slug = "%s-%s" % (orginal_slug, index)


class AJAXAutoCompleteTagsView(View):
    """
    AJAX: Returns tags
    """
    def get(self, request, *args, **kwargs):
        try:
            tags = Tag.objects.filter(
                name__istartswith=request.GET['query']
            ).values_list('name', flat=True)
        except MultiValueDictKeyError:
            tags = []

        return json_response({'suggestions': list(tags)})


class AJAXGetKeywordsView(LoginRequiredMixin, View):
    """
    AJAX: Returns keywords from the text
    Not yet implemented
    """
    def get(self, request, *args, **kwargs):
        keywords = request.GET['text']
        return json_response({'keywords': keywords})
