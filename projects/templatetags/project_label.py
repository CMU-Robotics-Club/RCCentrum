from django.conf import settings
from django.template import Library

from PIL import Image, ImageDraw, ImageFont
from os import path
import hashlib
import os

FONT_DIR = os.path.join(settings.STATIC_ROOT, "fonts")
IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, "project_labels")

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def create_font(filename, size):
    font_path = os.path.join(FONT_DIR, filename)
    return ImageFont.truetype(font_path, size)

def create_label(path, project):
    font_light_text = "Carnegie Mellon Robotics Club"
    font_light = create_font("Roboto-Thin.ttf", 300)
    font_light_color = "#000000"
    font_light_w, font_light_h = font_light.getsize(font_light_text)
    url_x, url_y = font_light.getsize(project.website)

    font_bold_text = "Official Club Project"
    font_bold = create_font("Roboto-Regular.ttf", 300)
    font_bold_color = "#000000"
    font_bold_w, font_bold_h = font_bold.getsize(font_bold_text)

    font_project = create_font("Roboto-Regular.ttf", 600)
    font_project_color = "#0000AA"
    font_project_w, font_project_h = font_project.getsize(project.name)

    w = max((font_light_w + font_bold_w) + 250, url_x)
    h = (font_light_h + font_project_h + url_y/2 + 100)

    img = Image.new('RGBA', (int(w), int(1.4*h)), "#ffffff")
    draw = ImageDraw.Draw(img)

    draw.text((0,0), font_light_text, font=font_light, fill=font_light_color)
    draw.rectangle([(font_light_w+100,0),(font_light_w+150,font_light_h)], fill="#aaaaaa")
    draw.text((font_light_w+150+100,0), font_bold_text, font=font_bold, fill=font_bold_color)

    draw.text((w/2 - font_project_w/2,h/2 - font_project_h/2), project.name, font=font_project, fill=font_project_color)

    draw.text((w/2 - url_x/2, h/2 + font_project_h/2 + 100), project.website, font=font_light, fill=font_light_color)

    img.save(path,"JPEG",quality=100)  


register = Library()

@register.filter
def project_label(project):
    '''
    Usage:
    {{project|project_label|safe}}
    '''

    label_filename = "{}.jpg".format(project)
    label_path = os.path.join(IMAGE_DIR, label_filename)

    if path.exists(label_path):
        pass
    else:
        create_label(label_path, project) 
    
    label_url = "{}{}/{}".format(settings.MEDIA_URL, "project_labels", label_filename)
    link = '<a href="{}" target="_blank" >Project Label</a>'.format(label_url)
    return link
