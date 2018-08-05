############################################################### LIBRARIES ###############################################################

import os
import yaml
import json
import requests


from boxsdk import Client, OAuth2


############################################################### CREATE CLIENT ###############################################################

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


############################################################### WORKING FUNCTIONS ###############################################################


# function takes folder id, client object, and prints folder info
# get_folder_info('40299062100',client) #40299062100 = folder ID for DSP Revenue Files
def get_folder_info(id,client):
	dsp_rev_root = client.folder(folder_id = id).get()
	print dsp_rev_root

# Below function lets user search for a keyword and then return list of values for either file or folder

def search_box():
	limit=100
	offset=0
	search_term = raw_input('Search for: ')
	type = raw_input('Type (Folder, File, Web Link): ')
	content = client.search(search_term, result_type=type, limit=limit, offset=offset)
	print content

#search_box(limit=10,offset=0)

# Gets all items in a folder and prints folder IDs which are stored in text doc (root: '40299062100')

def get_all_items_in_folder_to_txt(id):
	#gets all items
	root_folder_items = client.folder(folder_id=id).get_items(limit=100, offset=0)

	#writes to folder
	#writes folder items to text document and trims the <box folder> string from output
	with open('items.txt', 'wb') as f:
		for x in root_folder_items:
			x = str(x)
			f.write(x[14:] + '\n')
			
		f.close()

#Get all items in folder, I used this for file ids to download

def get_all_items_in_folder(id):
	#gets all items
	root_folder_items = client.folder(folder_id=id).get_items(limit=100, offset=0)

	return root_folder_items

#can be used to retrieve folder or file ids from directory. requires a folder id


def clean_file_name(file):

	unwanted_chars = ['(',')','>','<']
	#remove unwanted characters
	for char in unwanted_chars:
		if char in file:
			file = file.replace(char,'')

	return file


def get_file_ids_from_folder_id(folder_id):

	items_to_iterate = get_all_items_in_folder(folder_id)
	items_list = {}
	#unwanted characters
	unwanted_chars = ['(',')','>','<']

	#split file data up
	#create a dict for each item name as key, item id as value
	for file in items_to_iterate :
		new_file = str(file).split(' ',4) #limit split to 5
		file_id = new_file[3]
		folder_name = new_file[4]
		#remove unwanted characters
		folder_name = clean_file_name(folder_name)
		items_list[folder_name] = file_id

	return items_list

# Read folder IDs from folder_configs (this needs to mantained manually)

def get_folder_ids_config():
	folder_dict = {}
	with open('folder_configs.yaml', 'r') as f:
		folder_dict = yaml.safe_load(f)
	#test
	#print folder_dict['RadiumOne']
	return folder_dict


#check for folder name in configuration file

def check_dsp_name(dsp_name):
	folder_dict = get_folder_ids_config()
	try:
		folder_dict[dsp_name]
		print dsp_name + " is an existing folder"
	except KeyError:
		print "DSP name does not exist. Please type exact name from Box"

#main function calls get_folder_ids_configs and check_dsp_name
def check_dsp_main():
	get_folder_ids_config()
	check_dsp_name('RadiumOne')


def upload_file(name,folder_id):
	#root path of files 
	path = 'C:/Users/Vishal Kumar/box_api_test/test_directory/'
	#full file path includes above path and file name appended
	#giving a file name will alter file extension, which we do not want
	file_path = path + name

	#NOTE: file_name is a parameter in the Box SDK for upload(), but it is must be left blank to ensure proper upload
	box_file = client.folder(folder_id).upload(file_path)


#file id and path is stored in config
#need to figure out a way to parse file ids from folder and pass into parameter
#sample adform file: 308172857070
#sample path: 
def download_dsp_file(id,path):
	with open (path, 'wb' ) as local_file:
		client.file(file_id=id).download_to(local_file)

#Type function you want to use here



