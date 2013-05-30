import hmac, base64, hashlib, urllib, requests
import time

BASE = 'https://data.mtgox.com/api/2/'
PAIR = 'BTCUSD'


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
            request = requests.post(BASE + path, data=params, headers=headers)
            return request.text
        except Exception as e:
            print '_request error: %s' % e

    """
    General information
    """

    def info(self):
        return self._request(PAIR + '/money/info')

    def idkey(self):
        return self._request(PAIR + '/money/idkey')

    def orders(self):
        return self._request(PAIR + '/money/orders')

    def currency(self):
        return self._request(PAIR + '/money/currency')

    def ticker(self):
        return self._request(PAIR + '/money/ticker')

    def ticker_fast(self):
        return self._request(PAIR + '/money/ticker_fast')

    """
    Orders
    """

    def order_quote(self, type, amount):
        params = { 'type': type, 'amount': amount }
        return self._request(PAIR + '/money/order/quote', params)

    def order_quote_bid(self, amount):
        return order_quote('bid', amount)

    def order_quote_ask(self, amount):
        return order_quote('ask', amount)

    def order_add(self, type, amount_int, price_int=None):
        params = { 'type': type, 'amount_int': amount_int }
        if price_int is not None:
            params['price_int'] = price_int
        return self._request(PAIR + '/money/order/add', params)

    def order_add_bid(self, amount_int, price_int=None):
        return order('bid', amount_int, price_int)

    def order_add_ask(self, amount_int, price_int=None):
        return order('ask', amount_int, price_int)

    def order_cancel(self, oid):
        params = { 'oid': oid }
        return self._request(PAIR + '/money/order/cancel', params)

    def order_result(self, type, order):
        params = { 'type': type, 'order': order }
        return self._request(PAIR + '/money/order/result', params)

    def order_result_bid(self, order):
        return order_result('bid', order)

    def order_result_ask(self, order):
        return order_result('ask', order)

    def order_lag(self):
        return self._request(PAIR + '/money/order/lag')

    """
    Trades
    """

    def trades_fetch(self, since=None):
        params = {}
        if since is not None:
            params['since'] = since
        return self._request(PAIR + '/money/trades/fetch', params)

    def trades_cancelled(self):
        return self._request(PAIR + '/money/trades/cancelled')

    """
    Depth
    """

    def depth_fetch(self):
        return self._request(PAIR + '/money/depth/fetch')

    def depth_full(self):
        return self._request(PAIR + '/money/depth/full')

    """
    Wallet
    """

    def wallet_history(self, currency, page=None):
        params = { 'currency': currency }
        if page is not None:
            params['page'] = page
        return self._request(PAIR + '/money/wallet/history')