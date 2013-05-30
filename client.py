# Copyright © 2013 albertyfwu <albertyfwu@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import hmac, base64, hashlib, urllib, requests
import time

BASE = 'https://data.mtgox.com/api/2/'
PAIR = 'BTCUSD'

class ClientException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Client:
    """
    Client for handling connections with
    MtGox server via MtGox trading API
    """

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
            response = requests.post(BASE + path, data=params, headers=headers)
            return json.loads(response.text)
        except Exception as e:
            print '_request error: %s' % e

    def _query(self, path, params={}):
        """
        Checks to see that returned JSON from
        _request is valid.
        """
        response = self._request(path, params):
        if 'result' in response and response['result'] == 'success':
            return response['data']
        else
            raise ClientException('Request failed')

    """
    General information
    """

    def info(self):
        return self._query(PAIR + '/money/info')

    def idkey(self):
        return self._query(PAIR + '/money/idkey')

    def orders(self):
        return self._query(PAIR + '/money/orders')

    def currency(self):
        return self._query(PAIR + '/money/currency')

    def ticker(self):
        return self._query(PAIR + '/money/ticker')

    def ticker_fast(self):
        return self._query(PAIR + '/money/ticker_fast')

    """
    Orders
    """

    def quote(self, type, amount):
        params = { 'type': type, 'amount': amount }
        return self._query(PAIR + '/money/order/quote', params)

    def quote_bid(self, amount):
        return order_quote('bid', amount)

    def quote_ask(self, amount):
        return order_quote('ask', amount)

    def order_add(self, type, amount_int, price_int=None):
        params = { 'type': type, 'amount_int': amount_int }
        if price_int is not None:
            params['price_int'] = price_int
        return self._query(PAIR + '/money/order/add', params)

    def bid(self, amount_int, price_int=None):
        return order_add('bid', amount_int, price_int)

    def ask(self, amount_int, price_int=None):
        return order_add('ask', amount_int, price_int)

    def order_cancel(self, oid):
        params = { 'oid': oid }
        return self._query(PAIR + '/money/order/cancel', params)

    def order_result(self, type, order):
        params = { 'type': type, 'order': order }
        return self._query(PAIR + '/money/order/result', params)

    def order_result_bid(self, order):
        return order_result('bid', order)

    def order_result_ask(self, order):
        return order_result('ask', order)

    def order_lag(self):
        return self._query(PAIR + '/money/order/lag')

    """
    Trades
    """

    def trades_fetch(self, since=None):
        params = {}
        if since is not None:
            params['since'] = since
        return self._query(PAIR + '/money/trades/fetch', params)

    def trades_cancelled(self):
        return self._query(PAIR + '/money/trades/cancelled')

    """
    Depth
    """

    def depth_fetch(self):
        return self._query(PAIR + '/money/depth/fetch')

    def depth_full(self):
        return self._query(PAIR + '/money/depth/full')

    """
    Wallet
    """

    def wallet_history(self, currency, page=None):
        params = { 'currency': currency }
        if page is not None:
            params['page'] = page
        return self._query(PAIR + '/money/wallet/history')