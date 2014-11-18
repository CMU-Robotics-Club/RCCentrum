from django.conf import settings

from PIL import Image, ImageDraw, ImageFont
from os import path
import hashlib
import os
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.text import slugify

FONT_DIR = os.path.join(settings.STATIC_ROOT, "fonts")
IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, "project_labels")

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def _load_font(filename, size):
    font_path = os.path.join(FONT_DIR, filename)
    return ImageFont.truetype(font_path, size)

font_light_text = "Carnegie Mellon Robotics Club"
font_light = _load_font("Roboto-Thin.ttf", 300)
font_light_color = "#000000"
font_light_w, font_light_h = font_light.getsize(font_light_text)

font_bold_text = "Official Club Project"
font_bold = _load_font("Roboto-Regular.ttf", 300)
font_bold_color = "#000000"
font_bold_w, font_bold_h = font_bold.getsize(font_bold_text)

font_project = _load_font("Roboto-Regular.ttf", 600)
font_project_color = "#0000AA"

def _create_label(path, project):
    url = "{}{}".format(str(Site.objects.get_current()), reverse('projects:detail-name', args=(slugify(project.name),)))
    url_x, url_y = font_light.getsize(url)

    font_project_w, font_project_h = font_project.getsize(project.name)

    w = max((font_light_w + font_bold_w) + 250, url_x)
    h = (font_light_h + font_project_h + url_y/2 + 100)

    img = Image.new('RGBA', (int(w), int(1.4*h)), "#ffffff")
    draw = ImageDraw.Draw(img)

    draw.text((0,0), font_light_text, font=font_light, fill=font_light_color)
    draw.rectangle([(font_light_w+100,0),(font_light_w+150,font_light_h)], fill="#aaaaaa")
    draw.text((font_light_w+150+100,0), font_bold_text, font=font_bold, fill=font_bold_color)

    draw.text((w/2 - font_project_w/2,h/2 - font_project_h/2), project.name, font=font_project, fill=font_project_color)

    draw.text((w/2 - url_x/2, h/2 + font_project_h/2 + 100), url, font=font_light, fill=font_light_color)

    img.save(path,"JPEG",quality=100)

def load_label(project):
    label_filename = "{}.jpg".format(slugify(project.name))
    label_path = os.path.join(IMAGE_DIR, label_filename)

    if path.exists(label_path):
        pass
    else:
        _create_label(label_path, project)

    return (label_filename, label_path)
