
import json
import requests

url = 'http://yxdemo.eastus.cloudapp.azure.com/Check/POC/tabukm/API/token'

head = {'Content-Type' : 'application/x-www-form-urlencoded'}    
auth_info = {'username' : 'automaticinspection',
            'password' : '123456',
            'grant_type' : 'password'
            }  

   

r = requests.post(url, auth_info, head)

response=json.loads(r.text)
token = response['access_token']
response_dict = {"status_code":r.status_code,"access_token":token}
print(response_dict)
