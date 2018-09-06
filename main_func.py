############################################################### LIBRARIES ###############################################################

import os
import yaml
import requests
from StringIO import StringIO
from datetime import datetime

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


def get_folder_info(id,client):
	'''
	function takes folder id, client object, and prints folder info
    get_folder_info('40299062100',client) #40299062100 = folder ID for DSP Revenue Files
	'''
	dsp_rev_root = client.folder(folder_id = id).get()
	print dsp_rev_root

def search_box():
	'''
	Below function lets user search for a keyword and then return list of values for either file or folder
	'''
	limit=100
	offset=0
	search_term = raw_input('Search for: ')
	type = raw_input('Type (Folder, File, Web Link): ')
	content = client.search(search_term, result_type=type, limit=limit, offset=offset)
	print content

#search_box(limit=10,offset=0)


def get_all_items_in_folder_to_txt(id):
	'''
	Gets all items in a folder and prints folder IDs which are stored in text doc (root: '40299062100')
	'''
	#gets all items
	root_folder_items = client.folder(folder_id=id).get_items(limit=100, offset=0)

	#writes to folder
	#writes folder items to text document and trims the <box folder> string from output
	with open('items.txt', 'wb') as f:
		for x in root_folder_items:
			x = str(x)
			f.write(x[14:] + '\n')
			
		f.close()

def get_all_items_in_folder(id):
	'''
	#Get all items in folder, I used this for file ids to download
	'''
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

def get_folder_ids_from_config():
	'''
	Read folder IDs from folder_configs (this needs to mantained manually)
	'''
	folder_dict = {}
	with open('folder_configs.yaml', 'r') as f:
		folder_dict = yaml.safe_load(f)
	#test
	#print folder_dict['RadiumOne']
	return folder_dict

def check_dsp_name(dsp_name):
	'''
	check for folder name in configuration file
	'''
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


def upload_file_simple(name,folder_id):
	'''
	General template for uploading files from local directory to box
	'''
	#root path of files 
	path = 'C:/Users/Vishal Kumar/box_api_test/test_directory/'
	#full file path includes above path and file name appended
	#giving a file name will alter file extension, which we do not want
	file_path = path + name

	#NOTE: file_name is a parameter in the Box SDK for upload(), but it is must be left blank to ensure proper upload
	box_file = client.folder(folder_id).upload(file_path)


def get_file_names(id):
	'''
	This function
	params: id = folder_id
	returns: names of files in folder
	Sample Folder ID for Adelphic: 40299155116 
	'''
	root_folder_items = client.folder(folder_id=id).get_items(limit=100, offset=0)

	for item in root_folder_items:
		type = client.file(file_id=item['type'])
		if str(type) != '<Box File - folder>':
			#line below gets file name
			name = client.file(file_id=item['id']).get()['name']
			print 'Name: %s' %name

def download_file(id):
	'''
	takes in file id and downloads file to given path
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
	with open('C:/Users/Vishal Kumar/box_api_test/test_directory/' + file_name, 'wb') as f:
		f.write(my_file)

def get_dsp_files_search():
	'''
	takes user input for DSP folder name and fetches all file names if folder exists
	can be re-used to download files instead of fetch names
	'''
	file_name = raw_input('Enter file name: ')

	folders = func.get_folder_ids_from_config()

	for key, value in folders.iteritems():
		#key = dsp folder name from folder_configs.yaml
		#value = folder id from folder_configs.yaml
		if file_name == str(key):
			try:
				func.get_file_names(value)
			except:
				print "File does not exist"

def get_dsp_file_create_dates(id):
	'''
	This function grabs the created on date for each file in folder
	params: id = folder_id
	returns: created on dates of files in folder
	Sample ID for Adelphic: 40299155116 
	'''
	root_folder_items = client.folder(folder_id=id).get_items(limit=100, offset=0)

	date_times_list = []
	
	for item in root_folder_items:
		type = client.file(file_id=item['type'])
		if str(type) != '<Box File - folder>':
			#line below gets file name
			created_at =  client.file(item['id']).get()['created_at']
			#first 11 characters make up YYYY-MM-DD from the above request
			created_on_date = created_at[0:10]
			#replace - with / 
			created_on_date = created_on_date.replace('-','/')
			#convert string into datetime
			created_on_date_formatted = datetime.strptime(created_on_date, '%Y/%m/%d')
			date_times_list.append(created_on_date_formatted)
		return max(date_times_list)


#this is a success. we can further improve by entering parameters via command line...do some research later. Not urgent but will be useful.
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

	box_file = client.folder(id).upload(file_path)

#Type function you want to use here



