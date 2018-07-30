############################################################### LIBRARIES ###############################################################

import os
import yaml
import json
import requests
import maintenance_functions as func

try:
	from boxsdk import Client, OAuth2
	
except importError:
			print "1 or more module has failed"
else:
	print "Module imported succesfully"

############################################################### CREATE CLIENT ###############################################################

#Below scripts taken from http://opensource.box.com/box-python-sdk/tutorials/intro.html
#We will use the developer token for quick testing and integration

# Define client ID, client secret, and developer token.
CLIENT_ID = None
CLIENT_SECRET = None
ACCESS_TOKEN = None

# Read configuation file app.yaml
with open('app.yaml', 'r') as f:
    config_file = yaml.safe_load(f)

    CLIENT_ID = config_file['client_id']
    CLIENT_SECRET = config_file['client_secret']
    ACCESS_TOKEN = config_file['developer_token']

oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)

#Create new client object
client = Client(oauth2)


#################################################################TESTING BELOW#################################################################
#################################################################TESTING BELOW#################################################################
#################################################################TESTING BELOW#################################################################

# Set upload values

#PATH TO LOCAL FILE TO BE UPLOADED

file_path = os.path.normpath('C://Users//VishalKumar/box_api_test//test_directory//')
#FILE NAME TO UPLOAD AS
file_name = 'AdForm IntegralAds - BS 06 2018'
#FOLDER ID TO UPLOAD TO
folder_id = 51939231352

box_file = client.folder(folder_id).upload(file_path, file_name)

