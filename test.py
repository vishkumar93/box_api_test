#test python
import os

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
with open('app.cfg', 'r') as app_cfg:
    CLIENT_ID = app_cfg.readline()
    CLIENT_SECRET = app_cfg.readline()
    ACCESS_TOKEN = app_cfg.readline()
	


from boxsdk.network.default_network import DefaultNetwork
from pprint import pformat

class LoggingNetwork(DefaultNetwork):
    def request(self, method, url, access_token, **kwargs):
        """ Base class override. Pretty-prints outgoing requests and incoming responses. """
        print '\x1b[36m{} {} {}\x1b[0m'.format(method, url, pformat(kwargs))
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

# At this point, the SDK Client is fully authenticated


# Upload a file to Box! It works.

# Upload a file to Box, with Error handling for duplicate file names

#file_path = os.path.normpath("C:/Users/Vishal/Desktop/get_response.csv")

file_name = "get_response.csv"

from StringIO import StringIO
stream = StringIO()
stream.seek(0)
from boxsdk.exception import BoxAPIException
try:
    box_file = client.folder('40972602395').upload_stream(stream, file_name, preflight_check=True)
except BoxAPIException:
    pass

# Get folder info

# items = client.folder(folder_id='40972602395').get_items(limit=100, offset=0)



#test folder
#{"type":"folder","id":"40972602395","sequence_id":"0","etag":"0","name":"Insights Test Folder"}


