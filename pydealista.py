"""Idealista Explorer

Use the idealista.com API to run queries
(c) 2017 Marcelo Novaes
"""

import argparse
import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth

# Sets the name to look for enviroment variables
ENV_API_KEY = "IDEALISTA_API_KEY"
ENV_API_SECRET = "IDEALISTA_API_SECRET"


def get_oauth_token(key, secret):
    """Gets oauth2 token from the API Key and Secret provided by idealista
    """
    oauth_url = "https://api.idealista.com/oauth/token"
    payload = {"grant_type": "client_credentials"}
    r = requests.post(oauth_url,
                      auth=HTTPBasicAuth(key, secret),
                      data=payload)
    # print(r.text)
    return r.text

def search_api(url, token):
    """Runs a search using the API and a token
    """
    # api_url = "http://api.idealista.com/3.5/es/search?center=40.42938099999995,-3.7097526269835726&country=es&maxItems=500&numPage=1&distance=452&propertyType=bedrooms&operation=rent"
    api_url = url
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(api_url,
                      headers=headers)
    # print(r.text)
    return r.text


# TODO if __name__ == "__main__":

# Parse arguments from command-line
parser = argparse.ArgumentParser(description="Arguments for Idealista API")
parser.add_argument("url")
parser.add_argument("country")
# parser.add_argument("parameters", nargs="*")
args = parser.parse_args()

print("URL provided: {}".format(args.url))
url_value = args.url
# print("~ Nums: {}".format(args.parameters))

# Get idealista API key and secret from environment variables
api_key = os.environ.get(ENV_API_KEY)
if api_key:
    print("Idealista API key loaded from environment: " + api_key)
else:
    print("No Idealista API key found as environment variable " + ENV_API_KEY)
api_secret = os.environ.get(ENV_API_SECRET)
if api_secret:
    print("Idealista API secret loaded from environment: " + api_secret)
else:
    print("No Idealista API secret found as environment variable " + ENV_API_SECRET)

token_json = get_oauth_token(api_key, api_secret)
token_response = json.loads(token_json)
token_value = token_response["access_token"]
print("Token: " + token_value)
search_json = search_api(url_value, token_value)
search_response = json.loads(search_json)
search_pretty = json.dumps(search_response, indent=4, sort_keys=True)
print(search_response)

with open("data/idealista_json_" + time.strftime("%Y-%m-%d_%H-%M") + ".json", 'w') as export:
    json.dump(search_pretty, export)
