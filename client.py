import hmac, base64, hashlib, urllib, requests
import time

base = 'https://data.mtgox.com/api/2/'

class Client:

    def __init__(self, key, secret):
        self.key = key
        self.secret = base64.b64decode(secret)

    def _nonce(self):
        return str(int(time.time() * 1e6))

    def _request(self, path, params={}):
        params['nonce'] = self._nonce()
        data = urllib.urlencode(params)
        hash_data = path + chr(0) + data
        sha512 = hashlib.sha512
        sign = base64.b64encode(str(hmac.new(self.secret, hash_data, sha512).digest()))

        headers = {
            'User-Agent': 'mtgox-trader',
            'Rest-Key': self.key,
            'Rest-Sign': sign
        }

        try:
            request = requests.post(base + path, data=params, headers=headers)
            return request.text
        except Exception as e:
            print e

    def doStuff(self):
        print self._request('BTCUSD/money/ticker')