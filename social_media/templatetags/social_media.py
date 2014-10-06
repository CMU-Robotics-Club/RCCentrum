from django import template
from django.conf import settings
from ..models import SocialMedia
from django.contrib.sites.shortcuts import get_current_site

register = template.Library()

# TODO: refactor this file so its not a condensed version of OrderedFlatPages

class SocialMediaNode(template.Node):
    def __init__(self, context_name, starts_with=None, user=None):
        self.context_name = context_name

    def render(self, context):
        social_medias = SocialMedia.objects.all()
        context[self.context_name] = social_medias
        return ''


@register.tag
def get_social_medias(parser, token):
    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "['url_starts_with'] [for user] as context_name" %
                      dict(tag_name=bits[0]))
    # Must have at 3-6 bits in the tag
    if len(bits) >= 3 and len(bits) <= 6:

        # If there's an even number of bits, there's no prefix
        if len(bits) % 2 == 0:
            prefix = bits[1]
        else:
            prefix = None

        # The very last bit must be the context name
        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        context_name = bits[-1]

        # If there are 5 or 6 bits, there is a user defined
        if len(bits) >= 5:
            if bits[-4] != 'for':
                raise template.TemplateSyntaxError(syntax_message)
            user = bits[-3]
        else:
            user = None

        return SocialMediaNode(context_name, starts_with=prefix, user=user)
    else:
        raise template.TemplateSyntaxError(syntax_message)