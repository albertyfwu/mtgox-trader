import json

from client import Client

api = json.load(open('./api_info.json'))
MTGOX_KEY = api['MTGOX_KEY']
MTGOX_SECRET = api['MTGOX_SECRET']

client = Client(MTGOX_KEY, MTGOX_SECRET)
print client.ticker()