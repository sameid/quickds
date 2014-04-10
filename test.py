import json
import json
import urlparse
import urllib

url = "https://www.googleapis.com/analytics/v3/data/ga?ids=ga:00000001&dimensions=ga:month&metrics=ga:visitors,ga:avgTimeOnSite&filters=ga:country==Russia&start-date={date.startOfYear}&end-date={date.today}&max-results=10000"

def parse_url(_query, _key, _value):
    y = urlparse.urlparse(_query)
    z = urlparse.parse_qsl(y.query)
    for n,key in enumerate(z):
        if key[0] == _key:
            lst = list(key)
            lst[1] = _value
            key = tuple(lst)
            z[n] = key
    q = urllib.unquote(urllib.urlencode(z))
    new_url = urlparse.ParseResult(scheme=y.scheme, netloc=y.netloc, path=y.path, query=q, fragment=y.fragment, params=y.params)
    new_url = urlparse.urlunparse(new_url)
    return new_url


print parse_url(url, 'dimensions', 'poop')






