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
	#TODO: take fully qualified file name that includes local path and file name
	#	   add a try/except if local file exists
	local_path = 'C:/Users/Vishal Kumar/box_api_test/test_directory/'

	#full file path includes above path and file name appended
	#giving a file name will alter file extension, which we do not want
	file_path = local_path + name

	#NOTE: file_name is a parameter in the Box SDK for upload(), but it is must be left blank to ensure proper upload
	#Which folder should this file be uploaded to?
	#TODO: add a try except to catch if file exists. Box has a specific error for this.
	box_file = client.folder(id).upload(file_path)

	#TODO: Add a check for duplicate file to flag it, option to overwrite possibly?

	print 'File %s has been uploaded to Box in %s!' % (name, dsp_name)

#below function 
def get_file_names_and_download(dsp_name,requested_file_name):
	'''
	This function is a modification of get_file_names() as it stores file names in a list
	Utilizes these function: get_folder_ids_from_config() and download_file()
	Important: The requested file name MUST include the file extension
	params: dsp name is the folder and requested_file_name is the file to be downloaded
	returns: names of files in folder
	Sample Folder ID for Adelphic: 40299155116 
	'''
	#read folder ids from config file and returns folder_dict
	folder_dict = func.get_folder_ids_from_config()

	#try except to check if folder exists and then assigns folder id to variable
	try:
		print 'The folder requested exists with folder id: %s' %folder_dict[dsp_name]
		id = folder_dict[dsp_name]
	except:
		print 'DSP folder does not exist in Box or folder_configs.yaml'

	file_name_list = {}

	#
	root_folder_items = client.folder(folder_id=id).get_items(limit=100, offset=0)

	for item in root_folder_items:
		type = client.file(file_id=item['type'])
		if str(type) != '<Box File - folder>':
			#line below gets file name
			#TODO: try to verify if the requested file exists here instead of lines 171/172
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

#upload and download as a separate function, both functions will take parameters
#upload takes file name, dest of upload, whether you want to overwrite a parameter (boolean flag)

#download function: takes file name,returns the path of where you stored the file
#					break down into two functions: get list of files, download

#before calling these functions - inside the function we want to verify if source file, destination file exists

def search_box_for_id(folder_name):
	'''
	Below function lets user search for a keyword and then return list of values for either file or folder
	returns id
	#TODO: note for future development, add a check that these folders are under the root of DSP Files so that any duplicates are prevented
	'''
	limit=1
	offset=0
	type = 'Folder'
	content = client.search(folder_name, result_type=type, limit=limit, offset=offset)
	for item in content:
		folder_id = client.folder(folder_id=item['id']).get()['id']
		# dsp_id = client.folder(folder_id=item['id'])
		# print dsp_id['name']
	
	return folder_id

print search_box_for_id('Hotmob')