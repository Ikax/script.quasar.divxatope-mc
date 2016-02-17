# coding: utf-8
__author__ = 'mancuniancol'

class Browser:
    def __init__(self):
        import cookielib

        self._cookies = None
        self.cookies = cookielib.LWPCookieJar()
        self.content = None
        self.status = None

    def create_cookies(self, payload):
        import urllib

        self._cookies = urllib.urlencode(payload)

    def open(self, url='', language='en', payload={}):
        import urllib2

        result = True
        if len(payload) > 0:
            self.create_cookies(payload)
        if self._cookies is not None:
            req = urllib2.Request(url, self._cookies)
            self._cookies = None
        else:
            req = urllib2.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/39.0.2171.71 Safari/537.36')
        req.add_header('Content-Language', language)
        req.add_header("Accept-Encoding", "gzip")
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))  # open cookie jar
        try:
            response = opener.open(req)  # send cookies and open url
            # borrow from provider.py Steeve
            if response.headers.get("Content-Encoding", "") == "gzip":
                import zlib

                self.content = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(response.read())
            else:
                self.content = response.read()
            response.close()
            self.status = 200
        except urllib2.HTTPError as e:
            self.status = e.code
            result = False
        except urllib2.URLError as e:
            self.status = e.reason
            result = False
        return result

    def open2(self, url=''):
        import httplib

        word = url.split("://")
        search = word[1]
        pos = search.find("/")
        conn = httplib.HTTPConnection(search[:pos])
        conn.request("GET", search[pos:])
        r1 = conn.getresponse()
        self.status = str(r1.status) + " " + r1.reason
        self.content = r1.read()
        if r1.status == 200:
            return True
        else:
            return False

    def login(self, url, payload, word):
        result = False
        self.create_cookies(payload)
        if self.open(url):
            result = True
            data = self.content
            if word in data:
                self.status = 'Wrong Username or Password'
                result = False
        return result


browser = Browser()

query = "jurassic world"
url_search = "http://www.divxatope.com/buscar/descargas"
payload = {'categoria': '',
           'subcategoria': '',
           'idioma': '',
           'calidad': '',
           'ordenar': 'Fecha',
           'ord': 'Descendente',
           'search': query,
           'pg': ''}
browser.open(url_search, payload=payload)
print(browser.content)