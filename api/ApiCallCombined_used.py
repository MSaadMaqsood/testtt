
import json
import requests
from requests.structures import CaseInsensitiveDict

def apicallcombined_used(violation):

    url = 'http://yxdemo.eastus.cloudapp.azure.com/Check/POC/tabukm/API/token'

    head = {'Content-Type' : 'application/x-www-form-urlencoded'}
    auth_info = {'username' : 'automaticinspection',
                'password' : '123456',
                'grant_type' : 'password'
                }
    print("Post request to get token [sent]..")
    r = requests.post(url, auth_info, head)

    response=json.loads(r.text)
    token = response['access_token']
    response_dict = {"status_code":r.status_code,"access_token":token}
    print("Got the token ,Now sending post request with the token to get Data...")


    ############################ POST REQUEST FOR DATA USING THE TOKEN GENERATED ######################

    url = 'http://yxdemo.eastus.cloudapp.azure.com/Check/POC/tabukm/API/api/AutomaticInspection/CreateInspection'

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer "+response_dict['access_token']
    # headers["Content-Type"] = "application/json"

    data ={
    "OperationId": str(violation['op_id']),
      "FrameId": 0,
      "Case": 0,
      "TrackId": 0,
      "Long": violation['long'],
      "Lat": violation['lat'],
      "Date": violation['date'],
      "Time": violation['time'],
      "Speed": 0,
      "Temprature": "0",
      "Image": violation['display_img']
    }

    resp = requests.post(url, headers=headers, data=data)

    response_dict = {
        "status_code":resp.status_code,
        "Success":resp.json()['Success'],
        "Data":resp.json()['Data']
    }

    print(response_dict)









