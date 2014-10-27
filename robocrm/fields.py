from django.db import models

class CharNullField(models.CharField):
  description = "CharField that stores NULL but returns ''"

  def to_python(self, value):
    if isinstance(value, models.CharField):
      return value 
    if value == None:
      return ""
    else:
      return value
  
  def get_db_prep_value(self, value, connection, prepared=False):
    if value=="":
      return None
    else:
      return value
