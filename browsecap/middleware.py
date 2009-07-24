import time

from django.http import HttpResponseRedirect
from django.utils.http import cookie_date
from django.conf import settings

from browsecap.browser import is_mobile

# default cookie expire time is one month
DEFAULT_COOKIE_MAX_AGE = 3600*24*31

class MobileRedirectMiddleware(object):
    def process_request(self, request):
        if not getattr(settings, 'MOBILE_DOMAIN', False):
            return 

        # test for mobile browser
        if (
                # check for override cookie, do not check if present
                request.COOKIES.get('ismobile', '0') == '1' or (
                    # browser info present
                    'HTTP_USER_AGENT' in request.META
                    and 
                    # desktop browser override not set
                    request.COOKIES.get('isbrowser', '0') != '1' 
                    and 
                    # check browser type
                    is_mobile(request.META['HTTP_USER_AGENT'])
                )
            ):
            # redirect to mobile domain
            response = HttpResponseRedirect(settings.MOBILE_DOMAIN)

            # set cookie to identify the browser as mobile
            max_age = getattr(settings, 'MOBILE_COOKIE_MAX_AGE', DEFAULT_COOKIE_MAX_AGE)
            expires_time = time.time() + max_age
            expires = cookie_date(expires_time)
            response.set_cookie('ismobile', '1', domain=settings.SESSION_COOKIE_DOMAIN, max_age=max_age, expires=expires)
            return response

