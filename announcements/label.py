from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.text import slugify
from crm.label import Label

def create_announcement_label(announcement):
  label = Label()
  org_start, org_end = label.add_text("#000000", (0,0), "Roboto-Thin.ttf", 200, "Carnegie Mellon Robotics Club")
  rect_start, rect_end = label.add_rectangle("#aaaaaa", (org_end[0] + 20, 0), (20, org_end[1]))
  type_start, type_end = label.add_text("#000000", (rect_end[0] + 20, 0), "Roboto-Regular.ttf", 200, "Official Club Announcement")

  header_start, header_end = label.add_text_split("#0000AA", (int(type_end[0]/2), rect_end[1] + 80), "Roboto-Regular.ttf", 400, announcement.header, center_x=True, words_per_line=3)

  body_start, body_end = label.add_text_split("#000000", (int(type_end[0]/2), header_end[1] + 80), "Roboto-Thin.ttf", 200, announcement.body, center_x=True, words_per_line=5)

  return label.create()
