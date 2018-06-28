# box_api_test
This is all testing code for Box API Integration

How to Use:

app.cfg contains the CLIENT_ID, SECRET_ID, and DEVELOPER_TOKEN. Please update accordingly and this will get passed into the test.py script, which establishes the connection to Box SDK.

Next Steps for Vishal:

1) Clean up and make the test.py script as a separate "connector" script.
2) Establish another script which deals with uploading files from local directory to Box
3) Establish a Master script which imports the test.py and upload script, and then executes all
