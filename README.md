# searchTool

### Introduction  
This CLI tool is used for searching the related videos uploaded on YouTube given by the query term.
### Usage  
You should make the environments set up before running this CLI tool.  
* Python 2.7 or Python 3.5+
* The pip package management tool  
* The Google APIs Client Library for Python:    
  * pip install --upgrade google-api-python-client
* The google-auth-oauthlib and google-auth-httplib2 libraries for user authorization.    
  * pip install --upgrade google-auth-oauthlib google-auth-httplib2  

I test this search tool on ubuntu18.04 using python3.
   
python example.py (--query "query_term")  
### Results Format 
The search results will be saved to the csv file (default saved at the same folder) in the format of      
| title | upload_time | uploader | view_count |  
| ---------- | :----------: | :----------: | :----------: |
| titlexxx | xxxx-xx-xxTxx:xx:xxZ | channel_id | view_count | 
### Get more information about the YouTube API    
https://developers.google.com/youtube/v3/getting-started

