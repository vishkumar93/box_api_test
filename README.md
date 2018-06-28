# box_api_test
This is all testing code for Box API Integration

How to Use:

app.cfg contains the CLIENT_ID, SECRET_ID, and DEVELOPER_TOKEN. Please update accordingly and this will get passed into the test.py script, which establishes the connection to Box SDK.

Next Steps for Vishal:

1) Clean up and make the test.py script as a separate "connector" script.
2) Write scripts to do the following: 
      traverse thru directory structures?
      create a folder?
      create a file?
      access a file and copy locally?
      pass through link for a file or folder?
3) Establish a Master script which imports the test.py and various scripts, allows you to execute what you want to do
