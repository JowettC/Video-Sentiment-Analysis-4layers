
import requests, json
import os
import time
import requests


# File must be in the same directory 
def postRequest(filename):
    data = {
    'api_token': '7f9fb6ef0b39bed7ad74a03a5d14bd80',
    'return': 'apple_music,spotify',
    }
    
    path = os.path.join(os.getcwd(), "uploads" , filename)
    # print("path: " + os.getcwd())
    files = {
        'file': open(path, 'rb'),
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)
    data = json.loads(result.text)
    return data["result"]["artist"], data["result"]["title"]
