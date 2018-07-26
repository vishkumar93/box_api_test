#test python
import os
import yaml
import json
import requests

try:
	from boxsdk import Client, OAuth2
	
except importError:
			print "1 or more module has failed"
else:
	print "Module imported succesfully"

#Below scripts taken from http://opensource.box.com/box-python-sdk/tutorials/intro.html

# Define client ID, client secret, and developer token.
CLIENT_ID = None
CLIENT_SECRET = None
ACCESS_TOKEN = None

# Read app info from text file
with open('app.yaml', 'r') as f:
    config_file = yaml.safe_load(f)

    CLIENT_ID = config_file['client_id']
    CLIENT_SECRET = config_file['client_secret']
    ACCESS_TOKEN = config_file['developer_token']
	

# oauth = OAuth2(
#     client_id='CLIENT_ID',
#     client_secret='CLIENT_SECRET',
#     store_tokens='ACCESS_TOKEN'
# )

# auth_url, csrf_token = oauth.get_authorization_url('http://localhost')
    

from boxsdk.network.default_network import DefaultNetwork
from pprint import pformat

class LoggingNetwork(DefaultNetwork):
    def request(self, method, url, access_token, **kwargs):
        """ Base class override. Pretty-prints outgoing requests and incoming responses. """
        #print '\x1b[36m{} {} {}\x1b[0m'.format(method, url, pformat(kwargs))
        response = super(LoggingNetwork, self).request(
            method, url, access_token, **kwargs
        )
        if response.ok:
            print '\x1b[32m{}\x1b[0m'.format(response.content)
        else:
            print '\x1b[31m{}\n{}\n{}\x1b[0m'.format(
                response.status_code,
                response.headers,
                pformat(response.content),
            )
        return response

# Create OAuth2 object. It's already authenticated, thanks to the developer token.
oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)

# Create the authenticated client
client = Client(oauth2, LoggingNetwork())

dsp_rev_root = client.folder(folder_id = '40299062100').get()


#json.dumps(dsp_rev_root)