from crm.label import Label

def create_officer_label(officer):
  label = Label()
  name_start, name_end = label.add_text('#000000', (0,0), "Roboto-Thin.ttf", 200, officer.user.user.get_full_name())
  position_start, position_end = label.add_text('#000000', (int(name_end[0]/2), name_end[1]), "Roboto-Thin.ttf", 100, officer.position, center_x=True)
  image_start, image_end = label.add_image((int(name_end[0]/2) - 250, position_end[1] + 50), (500, 500), officer.image.path)

  memo = officer.memo
  memo_line_starts = []
  memo_line_ends = []
  
  if not memo:
    memo = ""
    memo_line_ends.append((-1, image_end[1]))

  l = memo.split()
  n = 5
  split_memo = [' '.join(l[x:x+n]) for x in range(0, len(l), n)]

  for s in split_memo:
    if memo_line_starts == []:
      start_y = image_end[1] + 50
    else:
      start_y = memo_line_ends[-1][1]

    memo_line_start, memo_line_end = label.add_text('#000000', (int(name_end[0]/2), start_y), "Roboto-Thin.ttf", 50, s, center_x=True)
 

    memo_line_starts.append(memo_line_start)
    memo_line_ends.append(memo_line_end)

  studies = "{} {}".format(officer.user.major, officer.user.grad_year)
  studies_start, studies_end = label.add_text('#000000', (name_end[0]/2, memo_line_ends[-1][1] + 50), "Roboto-Thin.ttf", 80, studies, center_x=True)

  return label.create()
