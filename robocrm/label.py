from datetime import datetime
from django.utils import formats
from crm.label import Label

def create_robouser_label(user):
  label = Label()
  org_start, org_end = label.add_text("#000000", (0,0), "Roboto-Thin.ttf", 200, "Carnegie Mellon Robotics Club")
  rect_start, rect_end = label.add_rectangle("#aaaaaa", (org_end[0] + 20, 0), (20, org_end[1]))
  type_start, type_end = label.add_text("#000000", (rect_end[0] + 20, 0), "Roboto-Regular.ttf", 200, "Personal Project")

  name_start, name_end = label.add_text("#0000AA", (type_end[0]/2, rect_end[1] + 80), "Roboto-Regular.ttf", 400, user.get_full_name(), True)

  email_start, email_end = label.add_text("#000000", (type_end[0]/2, name_end[1] + 80), "Roboto-Thin.ttf", 200, user.email, True)
  
  date_now = datetime.now()
  formatted_now = formats.date_format(date_now, "DATE_FORMAT")
  date_start, date_end = label.add_text("#000000", (type_end[0]/2, email_end[1] + 80), "Roboto-Thin.ttf", 200, formatted_now, True)
  
  return label.create()
