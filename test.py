############################################################### LIBRARIES ###############################################################

import os
import yaml
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

def upload_file(dsp_name,name):
	'''
	Takes dsp_name, which is the folder we want to upload to, and the name of the file we want to upload
	Please ensure that the name of the upload file includes extension, such as .xlsx or .csv
	Utilizes get_folder_ids_from_config() and the folder_configs.yaml

	'''

	#read folder folder configuration file
	folder_dict = func.get_folder_ids_from_config()

	#try except to check if folder exists and then assigns folder id to variable
	try:
		print 'The folder requested exists with folder id: %s' %folder_dict[dsp_name]
		id = folder_dict[dsp_name]
	except:
		print 'DSP folder does not exist in Box or folder_configs.yaml'

	#root path of files to be uploaded
	local_path = 'C:/Users/Vishal Kumar/box_api_test/test_directory/'

	#full file path includes above path and file name appended
	#giving a file name will alter file extension, which we do not want
	file_path = local_path + name

	#NOTE: file_name is a parameter in the Box SDK for upload(), but it is must be left blank to ensure proper upload
	#Which folder should this file be uploaded to?
	#TODO: add a try except to catch if file exists. Box has a specific error for this.
	box_file = client.folder(id).upload(file_path)

	print 'File %s has been uploaded to Box in %s!' % (name, dsp_name)

upload_file('DBM Test','Test - Dummy File.xlsx')