import json
import requests

url = 'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=AIzaSyDF7pv814Mjan6I4Gr0_BKZDYWsCjk7CuU'
payload = {'longDynamicLink': 'http://download.mobiletornado.com/android/GA/hot/'}
headers = {'content-type': 'application/json'}

r = requests.post(url, data=json.dumps(payload), headers=headers)
data = json.loads(r.text)
print 'f'