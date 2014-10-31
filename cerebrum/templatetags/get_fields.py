from django import template

register = template.Library()


class GetFieldsNode(template.Node):
    def __init__(self, object, context_name=None):
        self.object = template.Variable(object)
        self.context_name = context_name

    def render(self, context):
        object = self.object.resolve(context)
        fields = [(field.verbose_name, field.value_to_string(object))
                  for field in object._meta.fields]

        if self.context_name:
            context[self.context_name] = fields
            return ''
        else:
            return fields


@register.tag
def get_fields(parser, token):
    bits = token.split_contents()

    if len(bits) == 4 and bits[2] == 'as':
        return GetFieldsNode(bits[1], context_name=bits[3])
    elif len(bits) == 2:
        return GetFieldsNode(bits[1])
    else:
        raise template.TemplateSyntaxError(
            "get_fields expects a syntax of "
            "{% get_fields <object> [as <context_name>] %}")
