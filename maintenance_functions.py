############################################################### LIBRARIES ###############################################################

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


#function takes folder id, client object, and prints folder info
def get_folder_info(id,client):
	dsp_rev_root = client.folder(folder_id = id).get()
	print dsp_rev_root

# get_folder_info('40299062100',client)

#40299062100 = folder ID for DSP Revenue Files

# Below function lets user search for a keyword and then return list of values for either file or folder

def search_box(limit=10,offset=0):
	search_term = raw_input('Search for: ')
	content = client.search(search_term, limit=limit, offset=offset)
	print content

#search_box(limit=10,offset=0)

# #gets all items in a folder and prints folder IDs

def get_all_items_in_folder():
	#gets all items
	root_folder_items = client.folder(folder_id='40299062100').get_items(limit=100, offset=0)

	#writes to folder
	#writes folder items to text document and trims the <box folder> string from output
	with open('items.txt', 'wb') as f:
		for x in root_folder_items:
			x = str(x)
			f.write(x[14:] + '\n')
			
		f.close()


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


def check_dsp_main():
	get_folder_ids_config()
	check_dsp_name('RadiumOne')


#Type function you want to use here
get_all_items_in_folder()
