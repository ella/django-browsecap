from djangosanetesting import UnitTestCase

from browsecap.browser import is_mobile

class TestIsMobileDetection(UnitTestCase):
    mobile = [
            'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.13337/504; U; cs) Presto/2.2.0',
            'BlackBerry9000/4.6.0.126 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/170',
            'Mozilla/5.0 (PLAYSTATION 3; 1.00)',
            'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; cs-cz) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
            'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95/31.0.017; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
            'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
        ]
    desktop = [
            'Windows-RSS-Platform/2.0 (MSIE 8.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; GTB6; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.19) Gecko/20081202 Iceweasel/2.0.0.19 (Debian-2.0.0.19-0etch1)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.11) Gecko/2009060215 (CK-Stahuj.cz) Firefox/3.0.11 (.NET CLR 2.0.50727)',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; cs-cz) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/(null) Safari/525.27.1',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; cs; rv:1.9.0.11) Gecko/2009060214 Firefox/3.0.11',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.4.4',
            'Opera/9.64 (Windows NT 5.1; U; cs) Presto/2.1.1',
            'Opera/9.52 (X11; Linux i686; U; en)',
            'Wget/1.10.2',

        ]
    def test_returns_false_for_empty_user_agent(self):
        self.assert_false(is_mobile(''))

    def test_returns_false_for_unknown_browser(self):
        self.assert_false(is_mobile('Unknown'))

    def test_identify_known_desktop_browsers(self):
        fails = []
        for m in self.desktop:
            if is_mobile(m):
                fails.append(m)
        self.assert_equals([], fails)

    def test_identify_known_mobile_browsers(self):
        fails = []
        for m in self.mobile:
            if not is_mobile(m):
                fails.append(m)
        self.assert_equals([], fails)

