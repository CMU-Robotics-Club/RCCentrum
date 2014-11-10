from django.contrib import admin
from .models import Category, QA
from ordered_model.admin import OrderedModelAdmin
from django import forms
from tinymce.widgets import TinyMCE
from django.utils.text import slugify

class QAForm(forms.ModelForm):
  
  question = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 10}))
  answer = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 10}))

  class Meta:
    model = QA
    exclude = ()

class QAAdmin(admin.StackedInline):
  model = QA
  fields = ('question', 'answer', 'order', )
  list_display = ('question', 'answer', )
  extra = 1
  form  = QAForm

class CategoryAdmin(OrderedModelAdmin):
  fields = ('title', 'anchor', )
  readonly_fields = ['anchor', ]
  list_display = ('title', 'anchor', 'qas', 'move_up_down_links', )
  inlines = [QAAdmin]

  def qas(self, obj):
    qas = obj.qa_set.all()

    r = ''

    for qa in qas:
      r += '<p><b>{}</b>:  {}</p><br/>'.format(qa.question, qa.answer)

    return r
  qas.allow_tags = True
  qas.short_description = 'QAs'

  def anchor(self, obj):
    return slugify(obj.title)

admin.site.register(Category, CategoryAdmin)
