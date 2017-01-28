from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import StockItem

class StockItemAdmin(admin.ModelAdmin):
    fields = ('name', 'location', 'quantity', 'reorder_url', 'datasheet')
    list_display = ('name', 'location', 'quantity', 'reorder_url_safe', 'datasheet_safe')

    def reorder_url_safe(self, obj):
        if obj.reorder_url:
            return mark_safe("<a href={0} target=\"_blank\">{0}</a>".format(obj.reorder_url))
        else:
            return "(none)"
    reorder_url_safe.short_description = 'Reorder URL'

    def datasheet_safe(self, obj):
        if obj.datasheet.name:
            return mark_safe("<a href={0} target=\"_blank\">{1}</a>".format(obj.datasheet.url, obj.datasheet.name))
        else:
            return "(none)"
    datasheet_safe.short_description = 'Datasheet'

admin.site.register(StockItem, StockItemAdmin)
