from django import template
from django.contrib.admin.util import NestedObjects

from classytags.core import Tag, Options
from classytags.arguments import Argument, KeywordArgument
from classytags.helpers import AsTag, InclusionTag

register = template.Library()


class DisplayRelations(InclusionTag):

    options = Options(
        Argument('main_obj'),
    )

    template = 'templatetags/display_relations.html'

    def get_context(self, context, main_obj):
        '''
        collector = NestedObjects(using="default")
        collector.collect([main_obj])
        relations = collector.nested()
        import ipdb; ipdb.set_trace()
        '''
        links = [rel.get_accessor_name()
                 for rel in main_obj._meta.get_all_related_objects()]
        # import ipdb; ipdb.set_trace()
        for link in links:
            objOrMgr = getattr(main_obj, link)
            if objOrMgr.__class__.__name__ == 'RelatedManager':
                objects = objOrMgr.all()
            else:
                objects = [objOrMgr]
            for object in objects:
                print object

        return {'relations': ''}

register.tag(DisplayRelations)
