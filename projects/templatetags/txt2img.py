#
# Obtained from:
# https://djangosnippets.org/snippets/2737/
#

# TODO: move this out of projects app

from django.conf import settings
from django.template import Library

from PIL import Image, ImageDraw, ImageFont
from os import path
import hashlib
import os

register = Library()

@register.filter
def txt2img(text,font_size=14,bg="#ffffff",fg="#000000",font="sans-serif.ttf"):
    '''
    txt2img tag shows on the web text as images, helping to avoid get
    indexed email address and     some other information you don't want
    to be on search engines. Fonts should reside in the same folder of txt2img.
    
    Usage:
    {{worker.email|txt2img:18|safe}}
    '''
    font_dir = settings.MEDIA_ROOT+"/txt2img/"   # Set the directory to store the images

    if not os.path.exists(font_dir):
        os.makedirs(font_dir)

    img_name_temp = text+"-"+bg.strip("#")+"-"+fg.strip("#")+"-"+str(font_size) # Remove hashes
    img_name="{}.jpg".format(hashlib.md5(img_name_temp.encode('utf8')).hexdigest())

    if path.exists(font_dir+img_name): # Make sure img doesn't exist already
        pass
    else:
        try:
            font = ImageFont.truetype(font, font_size)
        except:
            font = ImageFont.load_default()

        w, h = font.getsize(text)
        img = Image.new('RGBA', (w, h), bg)
        draw = ImageDraw.Draw(img)
        draw.fontmode = "0" 
        draw.text((0,0), text, font=font, fill=fg)
        img.save(font_dir+img_name,"JPEG",quality=100)  
    imgtag = '<img src="'+settings.MEDIA_URL+'txt2img/'+img_name+'" alt="'+text+'" />'
    return imgtag
