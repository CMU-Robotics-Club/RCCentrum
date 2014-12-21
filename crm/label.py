import os
from django.conf import settings
from PIL import Image, ImageFont, ImageDraw

class Label(object):
  """
  Base class that defines functions
  used to create a roboclub image that
  will eventually be printed on paper.
  """

  def __init__(self):
    """
    Initialize a blank image.
    """

    self._image_dimensions = [50, 50]
    self._actions = []

  def get_text_dimensions(self, font_name, font_size, text):
    """
    Returns the dimensions of the string of text.
    """

    font_path = os.path.join(settings.FONT_ROOT, font_name)
    font = ImageFont.truetype(font_path, font_size)
    return font.getsize(text)

  def add_text(self, color, position, font_name, font_size, text, center_x=False):
    """
    Adds text to this image.
    """

    font_path = os.path.join(settings.FONT_ROOT, font_name)
    font = ImageFont.truetype(font_path, font_size)
    font_width, font_height = font.getsize(text)

    if center_x:
      position = (position[0] - int(font_width/2), position[1])

    x_start, y_start = position
    end_position = (x_start + font_width, y_start + font_height) 

    self._adjust_image_dimensions(end_position)

    f = lambda draw, image: draw.text(position, text, font=font, fill=color)
    self._actions.append(f)

    return (position, end_position)

  def add_rectangle(self, color, position, dimensions):
    """
    Adds a rectangle to this image.
    """

    x_start, y_start = position
    width, height = dimensions
    end_position = (x_start + width, y_start + height)

    self._adjust_image_dimensions(end_position)

    f = lambda draw, image: draw.rectangle([position, end_position], fill=color)

    self._actions.append(f)
    
    return (position, end_position)

  def add_image(self, position, dimensions, image_path):
    """
    Adds an image to this image.
    """

    end_position = (position[0] + dimensions[0], position[1] + dimensions[1])
    
    self._adjust_image_dimensions(end_position)

    image2 = Image.open(image_path)
    image2 = image2.resize(dimensions, Image.ANTIALIAS)

    f = lambda draw, image: image.paste(image2, (position[0], position[1]))

    self._actions.append(f)

    return (position, end_position)

  def create(self):
    """
    Creates and returns the 
    underlying Pillow/PIL image.
    """

    image_width, image_height = self._image_dimensions
    
    # Fixes bug on Linux where font getsize
    # underestimates
    image_height = int(1.2*image_height)

    image = Image.new('RGBA', (image_width, image_height), "#ffffff")

    draw = ImageDraw.Draw(image)

    for f in self._actions:
      f(draw, image)

    return image


  def _adjust_image_dimensions(self, end_position):
    """
    Private function that expands the internal dimension pair
    of the image to end_position if end_position is outside
    the current dimensions.
    """

    (x_end, y_end) = end_position

    if x_end > self._image_dimensions[0]:
      self._image_dimensions[0] = x_end

    if y_end > self._image_dimensions[1]:
      self._image_dimensions[1] = y_end