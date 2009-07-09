from ConfigParser import SafeConfigParser as ConfigParser
import re
import os

from django.core.cache import cache

CACHE_KEY = 'browsecap'
CACHE_TIMEOUT = 60*60*2 # 2 hours
BC_PATH = os.path.abspath(os.path.dirname(__file__ or os.getcwd()))

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
        data = cache.get(CACHE_KEY)
        if data:
            self.mobile_browsers = map(re.compile, data['mobile_browsers'])
            self.crawlers = map(re.compile, data['crawlers'])
            return

        cfg = ConfigParser()
        files = ("browscap.ini", "bupdate.ini")
        read_ok = cfg.read([os.path.join(BC_PATH, name) for name in files])
        if len(read_ok) == 0:
            raise IOError, "Could not read browscap.ini, " + \
                  "please get it from http://www.GaryKeith.com"

        browsers = {}
        parents = set()

        for name in cfg.sections():
            sec = dict(cfg.items(name))
            p = sec.get("parent")
            if p:
                parents.add(p)
            browsers[name] = sec

        self.mobile_browsers = []
        self.crawlers = []
        for name, conf in browsers.items():
            if name not in parents:
                p = conf.get('parent')
                if p:
                    parent = browsers[p]
                    conf.update(parent)

                if conf.get('ismobiledevice', 'false') == 'true' or conf.get('crawler', 'false') == 'true':
                    qname = re.escape(name)
                    qname = qname.replace("\\?", ".").replace("\\*", ".*?")
                    qname = "^%s$" % qname

                if conf.get('ismobiledevice', 'false') == 'true':
                    self.mobile_browsers.append(qname)

                if conf.get('crawler', 'false') == 'true':
                    self.crawlers.append(qname)

        cache.set(CACHE_KEY, {'mobile_browsers': self.mobile_browsers, 'crawlers': self.crawlers}, CACHE_TIMEOUT)

        self.mobile_browsers = map(re.compile, self.mobile_browsers)
        self.crawlers = map(re.compile, self.crawlers)

    def find_in_list(self, useragent, agent_list, cache):
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
        return self.find_in_list(useragent, self.mobile_browsers, self.mobile_cache)

    def is_crawler(self, useragent):
        return self.find_in_list(useragent, self.crawlers, self.crawler_cache)


browsers = MobileBrowserParser()

is_mobile = browsers.is_mobile
is_crawler = browsers.is_crawler


def update():
    import urllib
    urllib.urlretrieve("http://browsers.garykeith.com/stream.asp?BrowsCapINI",
                       "browscap.ini")


