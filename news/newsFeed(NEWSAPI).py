import http.client, urllib.parse



conn = http.client.HTTPSConnection('api.thenewsapi.com')

params = urllib.parse.urlencode({
    'api_token': 'wH7c1IBiNDYafVaEpWC09gndOr6V2SqnIGALjQ7n',
    'locale': 'us',
    'categories': 'sports',
    'limit': 3,
    })

conn.request('GET', '/v1/news/all?{}'.format(params))

res = conn.getresponse()
data = res.read()

print(data.decode('utf-8'))

APIresponse = data.decode('utf-8')

print(APIresponse["data"])
