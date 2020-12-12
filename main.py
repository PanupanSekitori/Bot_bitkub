import hashlib
import hmac
import json
import requests

# API info
API_HOST = 'https://api.bitkub.com'
API_KEY = ''
API_SECRET = ''

def json_encode(data):
	return json.dumps(data, separators=(',', ':'), sort_keys=True)

def sign(data):
	j = json_encode(data)
	#print('Signing payload: ' + j)
	h = hmac.new(API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
	return h.hexdigest()

# check server time
response = requests.get(API_HOST + '/api/servertime')
ts = int(response.text)
#print('Server time: ' + response.text)

# check balances
header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
}
data = {
	'ts': ts,
}
signature = sign(data)
data['sig'] = signature

#print('Payload with signature: ' + json_encode(data))
response = requests.post(API_HOST + '/api/market/balances', headers=header, data=json_encode(data))

#print('Balances: ' + response.text)
json_balances = json.loads(response.text)

#json_formatted_str = json.dumps(json_balances, indent=2)
json_balances_result = json_balances['result']
json_Balances_THB = json_balances_result['THB']
json_Balances_available = json_Balances_THB['available']

print("Balances THB: ",json_Balances_available)

#/////////////////////////////////////////////////////////////////////////////
market_ticker = requests.get(API_HOST + '/api/market/ticker')
json_data = json.loads(market_ticker.text)

json_formatted_str = json.dumps(json_data, indent=2)

print(json_formatted_str)