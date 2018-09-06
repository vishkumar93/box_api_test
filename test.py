############################################################### LIBRARIES ###############################################################

import os
import yaml
import json
import requests
import main_func as func
from StringIO import StringIO
from boxsdk.object.search import Search
from boxsdk.object.metadata import Metadata
from boxsdk.exception import BoxAPIException
from datetime import datetime

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


# with open ('C:\\Users\\Vishal Kumar\\new.xlsx', 'wb' ) as local_file:
#         #download sample Adform file to local path above
# 	client.file(file_id='308172857070').download_to(local_file)
# 	local_file.close()


# file = 'C:/Python27/blank.csv'
# client.file(file_id='308172857070').download_to(file)


#next step is find the metadata for when file was updated

#output = func.get_file_ids_from_folder_id(40299062100)



'''
So far here are the functions we need to use:

get_folder_ids_from_config() will return us the config file with folder names and folder ids

download_file() using the list from the get_folder_ids_from_config() func, we can download files in this folder

get_file_names() needs to be combined with download. If file name matches names in get_files_names, then download!
'''


def get_file_names_and_download(dsp_name,requested_file_name):
	'''
	This function is a modification of get_file_names() as it stores file names in a list
	Important: The requested file name MUST include the file extension
	params: dsp name is the folder and requested_file_name is the file to be downloaded
	returns: names of files in folder
	Sample Folder ID for Adelphic: 40299155116 
	'''
	#read folder ids from config file and returns folder_dict

	folder_dict = func.get_folder_ids_from_config()

	#perform a check to enforce that folder exists before moving on with function
	try:
		print 'The folder requested exists with folder id: %s' %folder_dict[dsp_name]
		id = folder_dict[dsp_name]
	except:
		print 'DSP folder does not exist in Box or folder_configs.yaml'

	file_name_list = {}

	root_folder_items = client.folder(folder_id=id).get_items(limit=100, offset=0)

	for item in root_folder_items:
		type = client.file(file_id=item['type'])
		if str(type) != '<Box File - folder>':
			#line below gets file name
			name = client.file(file_id=item['id']).get()['name']
			file_id = client.file(file_id=item['id']).get()['id']
			file_name_list[name] = file_id
			

	#file names stored as key, value pair and below code checks if name exists
	if requested_file_name in file_name_list:
		'''
		If the file exists, it will be downloaded. 
		The download directory is set in the download_file() func
		'''
		print '%s exists and can be downloaded' %requested_file_name
		print '...file is being downloaded'
		func.download_file(file_name_list[requested_file_name])
	else:
		print 'File does not exist in folder. Please check naming convention to confirm'


get_file_names_and_download('Adelphic','Adelphic 2016-12.xlsx')


'''
Sample ID for Adelphic: 40299155116

def file_exists_check()
	
	for file in folder id:
		get file name
'''