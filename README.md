# box_api_test
This is all testing code for Box API Integration

Configuration Files:

1) App: Contains Box API tokens
2) folder_configs: Contains Folder IDs to each DSP Revenue Folder
2) test_folder_configs: Contains a test folder to upload files

Code:

1) test.py: contains code to establish connection to Box API

        '''
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
        '''
2) main_func: Contains same code as above, but stores all completed functions, highlighted below:
 
3) main_func include the upload_file function:

  '''
  def upload_file(name,folder_id):
    #root path of files 
    path = 'C:/Users/Vishal Kumar/box_api_test/test_directory/'
    #full file path includes above path and file name appended
    #giving a file name will alter file extension, which we do not want
    file_path = path + name

    #NOTE: file_name is a parameter in the Box SDK for upload(), but it is must be left blank to ensure proper upload
    box_file = client.folder(folder_id).upload(file_path)
 '''





