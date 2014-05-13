import requests
import json
import csv
import sys
import urlparse
import urllib

a = sys.argv


if len(a) > 2:
    print 'Too many arguments provided'
    print 'Aborting...'
    sys.exit()

TYPE = 0
NAME = 1
FORMAT = 2
REFRESH = 3
OAUTH = 4
QUERY = 5

DYNAMIC = 6

config = open('./config.json').read()
_c = json.loads(config) #_c represents configuration

#################
## util functions specified with _*
input_file = _c['input']
if len(a) == 2:
    input_file = a[1]

def _get(req, host=_c['host']):
    res = requests.get(host+req, auth=(_c['user'],_c['pass']), verify=False)
    return res.json()

def _post(req, data, headers, host=_c['host']):
    res = requests.post(host+req, auth=(_c['user'],_c['pass']), data=json.dumps(data),headers=headers,verify=False)
    return res.json()

def _pprint(data):
    print ((json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))))
    return;

##################

setup_map = []

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

def build_query(query, data):
    for v in data:
        key = setup_map[data.index(v)]
        value = v
        query = parse_url(query, key, value)
    return query

def create_datasource(data):
    m = data[:DYNAMIC]
    q = data[DYNAMIC:]
    query = build_query(m[QUERY], q)
    oauth = m[OAUTH]
    oauth_ds = _get(req='/datasources/'+oauth+'?full=true')
    try:
        props = oauth_ds['data']['properties']
    except KeyError:
        print 'Invalid Datasource ID provided in OAuth field in '+ input_file
        print 'Aborting...'
        sys.exit()

    if m[TYPE] == 'google_analytics':
        payload_props = {
              "max_pages":1,
              "endpoint_url": query,
              "advancedQuery": query,
              "mode":"Advanced",
              "token_id":props['token_id'],
              "oauth_provider_id": props['oauth_provider_id'],
              "oauth_use_header": props['oauth_use_header'],
              "oauth_user_token": props['oauth_user_token']
              }
    elif m[TYPE] == 'facebook':
        payload_props = {
              "max_pages":1,
              "endpoint_url": query,
              "advancedQuery": query,
              "mode":"Advanced",
              "token_id":props['token_id'],
              "oauth_provider_id": props['oauth_provider_id'],
              "qtype": props['qtype'],
              "oauth_user_token": props['oauth_user_token']
              }

    payload = {
        "name":m[NAME],
        "description": "-",
        "format":m[FORMAT],
        "connector":m[TYPE],
        "refresh_interval":int(m[REFRESH]),
        "is_dynamic":False,
        "properties":payload_props
        }

    headers = { "Content-Type": "application/json"}
    r=_post(req='/datasources', data=payload, headers=headers)
    _pprint(r)

try:
    with open (input_file, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        ignore = True
        for row in reader:
            if not ignore:
                create_datasource(row)
            else:
                setup_map = row[DYNAMIC:]
            ignore = False
except IOError:
    print 'unable to read ' + input_file
    print 'Aborting...'
