from django.db import models
import os
from urllib.parse import urlparse

class StockItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
       
    # Location
    EBENCH = 'EB'
    SHOP   = 'SH'
    OTHER  = 'OT'
    LOCATION_CHOICES = (
        (EBENCH, 'eBench'),
        (SHOP,   'Shop'  ),
        (OTHER,  'Other' ),
    )
    location = models.CharField(max_length=2,
                                choices=LOCATION_CHOICES,
                                default=EBENCH)

    quantity = models.PositiveIntegerField(null=True, blank=True)

    reorder_url = models.URLField(max_length=255, null=True, blank=True)

    def datasheet_upload_to(instance, filename):
        _, extension = os.path.splitext(filename)
        safe_name = '-'.join(instance.name.split())
        return "datasheets/{}{}".format(safe_name, extension)

    datasheet = models.FileField(upload_to=datasheet_upload_to,
                                 null=True, blank=True)

    def get_reorder_url_domain(self):
        self.reorder_url_domain = urlparse(self.reorder_url).netloc


    def __str__(self):
        return self.name

