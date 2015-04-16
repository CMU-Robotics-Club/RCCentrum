from crm.label import Label

def create_officer_label(officer):
  label = Label()
  name_start, name_end = label.add_text('#000000', (0,0), "Roboto-Thin.ttf", 200, officer.user.user.get_full_name())
  position_start, position_end = label.add_text('#000000', (int(name_end[0]/2), name_end[1]), "Roboto-Thin.ttf", 100, officer.position, center_x=True)
  image_start, image_end = label.add_image((int(name_end[0]/2) - 500, position_end[1] + 50), (1000, 1000), officer.image.path)

  memo_start, memo_end = label.add_text_split('#000000', (int(name_end[0]/2), image_end[1] + 50), "Roboto-Thin.ttf", 50, officer.memo, center_x=True, words_per_line=5)

  studies = "{} {}".format(officer.user.major, officer.user.grad_year)
  studies_start, studies_end = label.add_text('#000000', (name_end[0]/2, memo_end[1] + 50), "Roboto-Thin.ttf", 80, studies, center_x=True)

  return label.create()
