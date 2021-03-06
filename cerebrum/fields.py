from django.template.loader import render_to_string
from django.utils.html import conditional_escape

from crispy_forms.layout import Field
from crispy_forms.layout import LayoutObject
from crispy_forms.utils import flatatt
from crispy_forms.utils import render_field


class FileField(Field):
    template = 'bootstrap3/layout/file_field.html'


class StatusField(Field):
    template = 'bootstrap3/layout/status_field.html'


class SlugField(Field):
    template = 'bootstrap3/layout/slug_field.html'


class ModalButton(LayoutObject):
    template = "%s/layout/modalbutton_field.html"

    def __init__(self, button_text, **kwargs):

        if hasattr(self, 'css_class') and 'css_class' in kwargs:
            self.css_class += ' %s' % kwargs.pop('css_class')
        if not hasattr(self, 'css_class'):
            self.css_class = kwargs.pop('css_class', None)

        self.css_id = kwargs.pop('css_id', '')
        self.template = kwargs.pop('template', self.template)
        self.modal_id = kwargs.pop('modal_id', '')
        self.content_source = kwargs.pop('content_source', '')
        self.flat_attrs = flatatt(kwargs)
        self.button_text = button_text

    def render(self, form, form_style, context,
               template_pack='bootstrap3', **kwargs):
        template = self.template % template_pack
        return render_to_string(template, {'div': self})
