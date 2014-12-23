from django.contrib.redirects.middleware import RedirectFallbackMiddleware
from django.http import HttpResponseRedirect

class TemporaryRedirectFallbackMiddleware(RedirectFallbackMiddleware):
  """
  Make redirects temporary (302) instead of permanent (303)
  since URLs will change depending upon semester (ex. /hackathon/).
  """

  response_redirect_class = HttpResponseRedirect
