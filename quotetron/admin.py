from django.contrib import admin
from .models import Quote
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.contrib.admin.util import unquote
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from functools import update_wrapper

class VoteableModelAdmin(admin.ModelAdmin):
  """
  Admin support for voteable models.
  """

  def upvote(self, obj):
    """
    Provide a button to upvote instance.
    """

    url = reverse("admin:{}_{}_upvote".format(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id, ))
    return mark_safe('<a href="{}"><div class="arrow-up"></div></a>'.format(url))
  upvote.short_description = 'Upvote'
  upvote.allow_tags = True

  def downvote(self, obj):
    """
    Provide a button to downvote instance.
    """
    
    url = reverse("admin:{}_{}_downvote".format(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id, ))
    return mark_safe('<a href="{}"><div class="arrow-down"></div></a>'.format(url))
  downvote.short_description = 'Downvote'
  downvote.allow_tags = True

  def upvote_view(self, request, obj_id):
    """
    Admin view to upvote object.
    """

    obj = get_object_or_404(self.model, pk=unquote(obj_id))
    obj.upvote()

    return HttpResponseRedirect('../../')

  def downvote_view(self, request, obj_id):
    """
    Admin view to downvote object.
    """

    obj = get_object_or_404(self.model, pk=unquote(obj_id))
    obj.downvote()

    return HttpResponseRedirect('../../')

  def get_urls(self):
    """
    Return default urls as well as those
    to upvote and downvote object.
    """

    urls = super().get_urls()

    def wrap(view):
      def wrapper(*args, **kwargs):
        return self.admin_site.admin_view(view)(*args, **kwargs)
      return update_wrapper(wrapper, view)

    return patterns('',
      url(r'^(.+)/upvote/$', wrap(self.upvote_view), name="{}_{}_upvote".format(self.model._meta.app_label, self.model._meta.model_name)),
      url(r'^(.+)/downvote/$', wrap(self.downvote_view), name="{}_{}_downvote".format(self.model._meta.app_label, self.model._meta.model_name)),
    ) + urls

  class Media:
    css = {
      'all': ('quotetron/css/voteable.css',)
    }


class QuoteAdmin(VoteableModelAdmin):

  fields = ('quote', )
  list_display = ('id', 'quote', 'upvote', 'up_votes', 'downvote', 'down_votes', 'votes', 'total_votes', )

  # Hides admin interface from Admin sidebar
  # Users can still visit the Admin Model URL
  # directly
  def get_model_perms(self, request):
    return {}

admin.site.register(Quote, QuoteAdmin)
