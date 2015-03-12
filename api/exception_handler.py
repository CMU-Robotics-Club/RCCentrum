from rest_framework.views import exception_handler

def api_exception_handler(exc, context):
  response = exception_handler(exc, context)

  if response is not None and hasattr(response, 'data'):
    if hasattr(exc, 'errno'):
      response.data['errno'] = exc.errno
    else:
      response.data['errno'] = -1

  return response
