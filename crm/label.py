import os
from django.conf import settings
from PIL import Image, ImageFont, ImageDraw

# TODO: fix bug where center_x can put
# text in location with negative x cordinates
# causing it not to be displayed.

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

    font_width, font_height = font.getsize(text)

    # Fixes bug on Linux where font getsize
    # underestimates
    # TODO: find a better way to do this
    font_height = int(1.2*font_height)

    return (font_width, font_height)

  def add_text(self, color, position, font_name, font_size, text, center_x=False):
    """
    Adds text to this image.
    """

    font_path = os.path.join(settings.FONT_ROOT, font_name)
    font = ImageFont.truetype(font_path, font_size)
    font_width, font_height = font.getsize(text)

    # Fixes bug on Linux where font getsize
    # underestimates
    # TODO: find a better way to do this
    font_height = int(1.2*font_height)

    if center_x:
      position = (position[0] - int(font_width/2), position[1])

    x_start, y_start = position
    end_position = (x_start + font_width, y_start + font_height) 

    self._adjust_image_dimensions(end_position)

    f = lambda draw, image: draw.text(position, text, font=font, fill=color)
    self._actions.append(f)

    return (position, end_position)


  def add_text_split(self, color, position, font_name, font_size, text, center_x=False, words_per_line=None):
    """
    Adds text to this image with max words_per_line words per line.
    If words_per_line is None all words are on on line(same functionality as add_text).
    """

    line_starts = []
    line_ends = []

    if not text:
        text = ""
        # End in the same place we begin if empty string
        line_ends.append(position)

    words = text.split()

    if not words_per_line:
        split_words = words
    else:
        split_words = [' '.join(words[x:x+words_per_line]) for x in range(0, len(words), words_per_line)]

    for s in split_words:
        if line_starts == []:
            start_y = position[1]
        else:
            start_y = line_ends[-1][1]

        line_start, line_end = self.add_text(color, (position[0], start_y), font_name, font_size, s, center_x)

        line_starts.append(line_start)
        line_ends.append(line_end)

    return (position, line_ends[-1])

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
