# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# `active` tag definition for the Cerebrum app.
# % use this tag to check if we are on the page that url is linking to
# (c) Twined/Univers 2009-2014. All rights reserved.
# ----------------------------------------------------------------------

from django import template

register = template.Library()


@register.tag
def active(parser, token):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1:])


class NavSelectedNode(template.Node):
    def __init__(self, patterns):
        self.patterns = patterns

    def render(self, context):
        if not 'request' in context:
            return ""

        path = context['request'].path
        for p in self.patterns:
            pValue = template.Variable(p).resolve(context)
            if path == pValue:
                return "active"
        return ""
