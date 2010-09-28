from djangosanetesting import UnitTestCase

from django.http import HttpRequest, HttpResponseRedirect
from django.conf import settings

from browsecap.middleware import MobileRedirectMiddleware

def build_request(user_agent='', cookies={}):
    """ 
    Returns request object with useful attributes
    """
    request = HttpRequest()
    # Session and cookies
    request.session = {}
    request.COOKIES = cookies
    request.META['HTTP_USER_AGENT'] = user_agent
    return request

class TestMobileRedirectMiddleware(UnitTestCase):
    def setUp(self):
        super(TestMobileRedirectMiddleware, self).setUp()
        settings.MOBILE_DOMAIN = 'http://mobile.example.com/'
        self.middleware = MobileRedirectMiddleware()

    def tearDown(self):
        super(TestMobileRedirectMiddleware, self).tearDown()
        if hasattr(settings, 'MOBILE_REDIRECT_PRESERVE_URL'):
            del settings.MOBILE_REDIRECT_PRESERVE_URL

    def test_does_nothing_if_mobile_domain_not_set(self):
        settings.MOBILE_DOMAIN = None
        response = self.middleware.process_request(build_request('Mozilla/5.0 (PLAYSTATION 3; 1.00)'))
        self.assert_equals(None, response)

    def test_does_nothing_for_desktop_browser(self):
        self.assert_equals(None, self.middleware.process_request(build_request()))

    def test_does_nothing_if_isbrowser_cookie_set(self):
        response = self.middleware.process_request(build_request('Mozilla/5.0 (PLAYSTATION 3; 1.00)', {'isbrowser': '1'}))
        self.assert_equals(None, response)

    def test_sets_cookie_for_mobile_browser(self):
        response = self.middleware.process_request(build_request('Mozilla/5.0 (PLAYSTATION 3; 1.00)'))
        self.assert_true('ismobile' in response.cookies)
        self.assert_equals('1', response.cookies['ismobile'].value)

    def test_redirects_for_mobile_browser(self):
        response = self.middleware.process_request(build_request('Mozilla/5.0 (PLAYSTATION 3; 1.00)'))
        self.assert_true(isinstance(response, HttpResponseRedirect))
        self.assert_equals(settings.MOBILE_DOMAIN, response['Location'])

    def test_redirects_if_ismobile_cookie_set(self):
        response = self.middleware.process_request(build_request(cookies={'ismobile': '1'}))
        self.assert_true(isinstance(response, HttpResponseRedirect))
        self.assert_equals(settings.MOBILE_DOMAIN, response['Location'])

    def test_redirects_if_ismobile_cookie_set(self):
        settings.MOBILE_REDIRECT_PRESERVE_URL = True
        request = build_request(cookies={'ismobile': '1'})
        request.path_info = '/some/url/'
        response = self.middleware.process_request(request)
        self.assert_true(isinstance(response, HttpResponseRedirect))
        self.assert_equals(settings.MOBILE_DOMAIN + 'some/url/', response['Location'])
