from rest_framework.views import exception_handler

def api_exception_handler(exc):
  response = exception_handler(exc)

  if response is not None and hasattr(exc, 'errno'):
    response.data['errno'] = exc.errno
  else:
    response.data['errno'] = -1

  return response
