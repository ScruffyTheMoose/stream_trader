from td.client import TDClient
import pprint

client_id = ''
redirect_uri = 'http://localhost'
json_path = 'C:/Users/Haze/Desktop/PyStuff/TDAAPI/tdaclientinfo.json'

# creats a new instance of the client
td_client = TDClient(client_id = client_id, redirect_uri = redirect_uri, credentials_path = json_path)

# log into a new session
td_client.login()

# get current quotes
option_chain = {
    'symbol': 'MSFT', 
    'contractType': 'ALL',
    'strikeCount': 3,
    'range': 'NTM',
    'includeQuotes': True,
    'fromDate': '2015-02-23',
    'afterDate': '2015-02-22',
    'strategy': 'SINGLE',
}
option_response = td_client.get_options_chain(option_chain)
pprint.pprint(option_response)