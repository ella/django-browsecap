from ConfigParser import SafeConfigParser as ConfigParser
import re
import os

from django.core.cache import cache
from django.conf import settings

CACHE_KEY = 'browsecap'
CACHE_TIMEOUT = 60*60*2 # 2 hours
DEFAULT_BC_PATH = os.path.abspath(os.path.dirname(__file__ or os.getcwd()))

class MobileBrowserParser(object):
    def __new__(cls, *args, **kwargs):
        # Only create one instance of this clas
        if "instance" not in cls.__dict__:
            cls.instance = object.__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.mobile_cache = {}
        self.crawler_cache = {}
        self.parse()

    def parse(self):
        # try egtting the parsed definitions from cache
        data = cache.get(CACHE_KEY)
        if data:
            self.mobile_browsers = map(re.compile, data['mobile_browsers'])
            self.crawlers = map(re.compile, data['crawlers'])
            return

        # parse browscap.ini
        cfg = ConfigParser()
        files = ("browscap.ini", "bupdate.ini")
        base_path = getattr(settings, 'BROWSCAP_DIR', DEFAULT_BC_PATH)
        read_ok = cfg.read([os.path.join(base_path, name) for name in files])
        if len(read_ok) == 0:
            raise IOError, "Could not read browscap.ini, " + \
                  "please get it from http://www.GaryKeith.com"

        browsers = {}
        parents = set()

        # go through all the browsers and record their parents
        for name in cfg.sections():
            sec = dict(cfg.items(name))
            p = sec.get("parent")
            if p:
                parents.add(p)
            browsers[name] = sec

        self.mobile_browsers = []
        self.crawlers = []
        for name, conf in browsers.items():
            # only process those that are not abstract parents
            if name in parents:
                continue

            p = conf.get('parent')
            if p:
                # update config based on parent's settings
                parent = browsers[p]
                conf.update(parent)

            # we only care for mobiles and crawlers
            if conf.get('ismobiledevice', 'false') == 'true' or conf.get('crawler', 'false') == 'true':
                qname = re.escape(name)
                qname = qname.replace("\\?", ".").replace("\\*", ".*?")
                qname = "^%s$" % qname

            # register the user agent
            if conf.get('ismobiledevice', 'false') == 'true':
                self.mobile_browsers.append(qname)

            if conf.get('crawler', 'false') == 'true':
                self.crawlers.append(qname)

        # store in cache to speed up next load
        cache.set(CACHE_KEY, {'mobile_browsers': self.mobile_browsers, 'crawlers': self.crawlers}, CACHE_TIMEOUT)

        # compile regexps
        self.mobile_browsers = map(re.compile, self.mobile_browsers)
        self.crawlers = map(re.compile, self.crawlers)

    def find_in_list(self, useragent, agent_list, cache):
        'Check useragent against agent_list of regexps.'
        try:
            return cache[useragent]
        except KeyError, e:
            pass

        for sec_pat in agent_list:
            if sec_pat.match(useragent):
                out = True
                break
        else:
            out = False
        cache[useragent] = out
        return out

    def is_mobile(self, useragent):
        'Returns True if the given useragent is a known mobile browser, False otherwise.'
        return self.find_in_list(useragent, self.mobile_browsers, self.mobile_cache)

    def is_crawler(self, useragent):
        'Returns True if the given useragent is a known crawler, False otherwise.'
        return self.find_in_list(useragent, self.crawlers, self.crawler_cache)


# instantiate the parser
browsers = MobileBrowserParser()

# provide access to methods as functions for convenience
is_mobile = browsers.is_mobile
is_crawler = browsers.is_crawler


def update():
    'Download new version of browsecap.ini'
    import urllib
    urllib.urlretrieve("http://browsers.garykeith.com/stream.asp?BrowsCapINI",
                       "browscap.ini")


