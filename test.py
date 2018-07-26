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
# convert below into function that takes a filename and where it will be uploaded as a paramater, and returns status of uploaded file
# have a root folder + base path + folder name for each DSP


# file_path = os.path.normpath("C:/Users/Vishal/Desktop/get_response.csv")

# file_name = "get_response.csv"

# from StringIO import StringIO
# stream = StringIO()
# stream.seek(0)
# from boxsdk.exception import BoxAPIException
# try:
#     box_file = client.folder('40972602395').upload_stream(stream, file_name, preflight_check=True)
# except BoxAPIException:
#     pass

#Get folder info
#we want to download file locally and return where we saved it


writeable_stream




dsp_rev_root = client.folder(folder_id = '40299062100').get()

shared_link = dsp_rev_root.get_shared_link_d

print shared_link

#download DSP file
# def dsp_folder_path(path,dsp_name):
#     dsp_root = client.folder(path['name'] + dsp_name



#root path for DSP files
root_path = os.path.normpath("C:/Users/Vishal Kumar/Box Sync/Insights/IAS Insights/Internal Deliverables/DSP Revenue/DSP Revenue Files/")

#move an item - i want to move from box to local
#client.file(file_id='SOME_FILE_ID').move(client.folder(folder_id='SOME_FOLDER_ID'))

# from the os library, we need to use normpath for Window's file path, as well as replace "/" with "/"
# right now i'm replacing slashes manually but I should just create another function to convert file paths

def traverse_local_dir(path):
    dir = []
    dsp_path = os.path.normpath(path)
    dir = os.listdir(dsp_path)

    for file in dir:
        print file

# path for files can go in a config file too for each individual DSP Directory
#for now this is for test
# path = ("C:/Users/Vishal Kumar/box_api_test/test_directory")
# traverse_local_dir(path)



