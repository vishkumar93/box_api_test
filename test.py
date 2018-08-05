############################################################### LIBRARIES ###############################################################

import os
import yaml
import json
import requests
import main_func as func

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

# Upload a file to Box! It works.

# Upload a file to Box, with Error handling for duplicate file names
# convert below into function that takes a filename and where it will be uploaded as a paramater, and returns status of uploaded file
# have a root folder + base path + folder name for each DSP

#### PLAN ####

#Check new file function (I need help with this one in terms of logic)

#Create a download file function

#Create an upload file function

# Set upload values





def get_file_ids_from_folder_id(folder_id):
	dbm_items = func.get_all_items_in_folder(folder_id)

	for file in dbm_items:
		new_file = str(file).split(' ',4) #limit split to 5
		
		break #i just want to download 1 for testing

	return new_file[3] #file id is 3rd object


# file = 'C:/Python27/blank.csv'
# client.file(file_id='308172857070').download_to(file)




# content() returns file as bytes 
file_contents = client.file(file_id='308172857070').content()




#file id and path is stored in config
#need to figure out a way to parse file ids from folder and pass into parameter
def download_dsp_file(id,path):
	with open (path, 'wb' ) as local_file:
		client.file(file_id=id).download_to(local_file)
		local_file.close()


download_dsp_file(308172857070,'C:\\Python27\\new.xlsx')
