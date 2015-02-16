from django.core.mail import send_mail

def subscribe_to_list(first_name, last_name, email, listname):
  if email == '':
    return

  name = first_name + ' ' + last_name

  if name == '':
    from_addr = email
  else:
    from_addr = '"' + name + '" <' + email + '>'

  to_addr = listname + '-subscribe@lists.andrew.cmu.edu'

  send_mail('', '', from_addr, [to_addr])
