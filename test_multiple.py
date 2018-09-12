############################################################### LIBRARIES ###############################################################

import os
import sys
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


def path_exits(file_path):
	local_file_exist_bool = os.path.exists(file_path)
	return local_file_exist_bool

def search_box_for_id(folder_name):
	'''
	Below function lets user search for a keyword and then return list of values for either file or folder
	returns id of folder if it exists
	#TODO: note for future development, add a check that these folders are under the root of DSP Files so that any duplicates are prevented
	'''
	limit=1
	offset=0
	type = 'Folder'
	
	content = client.search(folder_name, result_type=type, limit=limit, offset=offset)
	#Check in place for content, which is a list. If this is empty, no folders for the desired DSP will be found
	if not content:
		print 'No folders found'
		return None
	else:
		for item in content:
			folder_id = client.folder(folder_id=item['id']).get()['id']
			# dsp_id = client.folder(folder_id=item['id'])
			# print dsp_id['name']
	
		return folder_id

def upload_file(dsp_name,file_path):
	'''
	Takes dsp_name, which is the folder we want to upload to, and the name of the file we want to upload
	Please ensure that the name of the upload file includes extension, such as .xlsx or .csv
	Utilizes get_folder_ids_from_config() and the folder_configs.yaml
	'''
	#check if file exists
	#path_exits(file_path)
	if path_exits(file_path) is True:
		print "You have entered a valid file path. Script will continue."
		print "...."
	else:
		print "File does not exist. Script shutting down."
		sys.exit()

	#search_box_for_id() returns None if no folder was found, and a folder_id if folder was found
	
	if search_box_for_id(dsp_name) is not None:
		folder_id = search_box_for_id(dsp_name)
		print 'Destination folder requested exists with folder id: %s' %folder_id
		print '....'
	else:
		print 'Destination Folder does not exist. Script shutting down.'

	#NOTE: file_name is a parameter in the Box SDK for upload(), but it is must be left blank to ensure proper upload
	try:
		box_file = client.folder(folder_id).upload(file_path)
		print 'File %s has been uploaded to Box in %s!' % (file_path, dsp_name)
	#TODO: find a way to overwrite differently. For now we can delete the file.
	except BoxAPIException:
		print 'File already exists. Upload with new file name and run script again.'


#dummy path for PC with backslash converted: C:/Users/Vishal Kumar/box_api_test/test_directory/Test - Dummy File.xlsx
upload_file('DBM Test','C:/Users/Vishal Kumar/box_api_test/test_directory/Test - Dummy File.xlsx')


def get_file_name_dict(dsp_name):
	'''
	Takes the dsp folder name as paramater
	Utilizes search_box_for_id()
	Returns the file_name_list which is a dict
	'''

	if search_box_for_id(dsp_name) is not None:
		folder_id = search_box_for_id(dsp_name)
		print 'Destination folder requested exists with folder id: %s' %folder_id
		print '....'
	else:
		print 'Destination Folder does not exist. Script shutting down.'	

	root_folder_items = client.folder(folder_id=folder_id).get_items(limit=100, offset=0)

	file_name_dict = {}

	for item in root_folder_items:
		type = client.file(file_id=item['type'])
		if str(type) != '<Box File - folder>':
			#line below gets file name
			name = client.file(file_id=item['id']).get()['name']
			file_id = client.file(file_id=item['id']).get()['id']
			file_name_dict[name] = file_id

	return file_name_dict


#below function gets the file name and calls the download function
def main_download(dsp_name,requested_file_name):
	'''
    Main download function
	Utilizes these function: get_file_name_dict(),download_file()
	Important: The requested file name MUST include the file extension
	params: dsp name is the folder and requested_file_name is the file to be downloaded
	returns: names of files in folder
	Sample Folder ID for Adelphic: 40299155116 
	'''
	file_name_dict = get_file_name_dict(dsp_name)

	#file names stored as key, value pair and below code checks if name exists
	if requested_file_name in file_name_dict:
		'''
		If the file exists, it will be downloaded. 
		The download directory is set in the download_file() func
		'''
		save_path = func.download_file(file_name_dict[requested_file_name])
		
	else:
		print 'File does not exist in folder. Please check naming convention to confirm'

#upload and download as a separate function, both functions will take parameters
#upload takes file name, dest of upload, whether you want to overwrite a parameter (boolean flag)

#download function: takes file name,returns the path of where you stored the file
#					break down into two functions: get list of files, download

def download_file(id,save_path='C:/Users/Vishal Kumar/box_api_test/test_directory/'):
	'''
	takes in file id and downloads file to given path
	checks to see if file already exists in local path where it is to be downloaded
	sample adform file:308172857070
	'''
	stream = StringIO()
	stream.seek(0)

	# Download the file's contents from Box# 
	box_file = client.file(file_id=id).get()
	file_name = client.file(file_id=id).get()['name']
	my_file = box_file.content()
	stream.write(my_file)
	#path below can be changed to variable
	with open(save_path + file_name, 'wb') as f:
		new_save_path = save_path + file_name
		if path_exits(new_save_path) is True:
			print "This file already exists in the designated directory"
		else:
			f.write(my_file)
			print 'File is being downloaded to %s' %new_save_path

	return new_save_path

#main_download('DBM Test','Test - Dummy File.xlsx')