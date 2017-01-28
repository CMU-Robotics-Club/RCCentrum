from django.shortcuts import render
from .models import StockItem

def index(request):
  stock_items = []
  for loc_id, loc_title in StockItem.LOCATION_CHOICES:
      loc_items = StockItem.objects.filter(location=loc_id)
      for item in loc_items:
          item.get_reorder_url_domain()
      if len(loc_items) > 0:
          stock_items.append((loc_title, loc_items))

  return render(request, 'stock_items/index.jade',
                {'stock_items': stock_items})

