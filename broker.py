from td.client import TDClient
import httpx

API_KEY = open('tdakey.txt', 'r').read()
REDIRECT_URL = "http://localhost"
TOKEN_PATH = 'tda_creds.json'
SP500 = "https://tda-api.readthedocs.io/en/latest/_static/sp500.txt"

# creating client instance
td_client = TDClient(
    client_id=API_KEY,
    redirect_uri=REDIRECT_URL,
    credentials_path=TOKEN_PATH
)

# log into new client session
td_client.login()

# retrieving list of (outdated) SP500 companies
spy = httpx.get(SP500).read().decode().split()

