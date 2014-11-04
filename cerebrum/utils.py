# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Utility functions for the Cerebrum app
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

import json
from json import dumps, loads, JSONEncoder
import types
from urlparse import urlparse, parse_qs

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.db import models
from django.http import HttpResponse
from django.utils.functional import curry
from django.views.debug import SafeExceptionReporterFilter


class ExceptionReporterFilter(SafeExceptionReporterFilter):
    def get_traceback_frame_variables(self, request, tb_frame):
        cleansed_items = super(
            ExceptionReporterFilter, self).get_traceback_frame_variables(
                self, request, tb_frame
            )
        return cleansed_items


def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


def json_response(response_data):
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        return JSONEncoder.default(self, obj)


dumps = curry(dumps, cls=DjangoJSONEncoder)


def to_json(obj):
    if isinstance(obj, QuerySet):
        return dumps(obj)
        #return dumps(obj, cls=DjangoJSONEncoder)
    if isinstance(obj, models.Model):
        # do the same as above by making it a queryset first
        set_obj = [obj]
        set_str = dumps(loads(serialize('json', set_obj)))
        # eliminate brackets in the beginning and the end
        str_obj = set_str[1:len(set_str) - 2]
    return str_obj


def merge_settings(default_settings, user_settings):
    # store a copy of default_settings, but overwrite with
    # user_settings's values where applicable
    merged = dict(default_settings, **user_settings)
    default_settings_keys = default_settings.keys()

    # if the value of merged[key] was overwritten with
    # user_settings[key]'s value then we need to put back any
    # missing default_settings[key] values
    for key in default_settings_keys:
        # if this key is a dictionary, recurse
        if isinstance(default_settings[key],
                      types.DictType) and key in user_settings:
            merged[key] = merge_settings(
                default_settings[key],
                user_settings[key]
            )

    return merged
