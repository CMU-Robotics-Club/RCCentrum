import requests

def remote_lookup(upc):
  """
  Returns the name of the item with the specified UPC.
  Returns None if the item is not found.
  `upc` should always be formatted first by passing the result
  of `format_upc`. 
  """

  r = requests.get("http://www.upcdatabase.com/item/{}".format(upc))

  m = r.text
  
  # TODO: clean this up

  # If this is found, the UPC lookup was successful
  anchor = "Description"

  try:
    i = m.index(anchor)+len(anchor)
    b = m[i + 3*len("</td>") + len("<td>") - 1:]
    e = b.index("</td>")
  except:
    return None

  return b[:e]
