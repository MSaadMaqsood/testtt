import time
import cv2
import base64
import requests
import random
from requests import request
import csv
from datetime import datetime
from upload_api_03 import *

filename_upload = input("Input filename (name.csv): ")
uploading_date = input("Input Date (YYYY-MM-DD): ")
print("\nSetting up violations!!")
try:
    tttttt = []
    with open(filename_upload, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for vio in csvreader:
            if str(vio[2]) == '' and str(vio[0]) == '':
                break
            img = cv2.imread('to_upload_img/'+str(vio[2])+".jpg")
            string_img = base64.b64encode(
                cv2.imencode('.jpg', img)[1]).decode()

            temp = {
                "street_id": 0,
                "street_name": "",

                "violation_type_id": 0,
                "violation": vio[0],

                "details": "Tree",
                "accurate": vio[1],
                "risk": 0,
                "display_img": str(vio[2]) + ".jpg",
                "string_img": string_img,

                "lat": float(vio[3].split(',')[0]),
                "lng": float(vio[3].split(',')[1]),

                "violation_date": uploading_date,
                "violation_time": "14:15",
                "correct": 1,
                "device_id": 1,
                "polygon_img": "0",
                "super_violation_id": 0,
            }
            tttttt.append(temp)
except:
    print("Failed to setup violations!!!!!")
    input('Press any key to exit!!')
    exit()

print("Ready to GO!!")
try:
    print("\nTimer Started!!")
    x = time.perf_counter()
    print("Processing Please Wait.............\n")
    pending = main_function(tttttt, uploading_date)
    print("\nProcessing Complete.")
    print("\tTime Consume in Sec: ", time.perf_counter() - x)

except:
    print("Failed in processing!!!!!")
    input('Press any key to exit!!')
    exit()

try:
    if len(pending) > 0:
        now = datetime.now()
        current_time = now.strftime("%b_%d_%Y_%H_%M_%S")

        filename = current_time+".csv"
        with open('pending/'+filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Violation Type", "Accurate",
                               "Display img(without .jpg)", "lat, long", "Date (YYYY-MM-DD)"])

            for i in pending:
                csvwriter.writerow([i['violation'], i['accurate'], i['display_img'].split('.')[
                                   0], str(i['lat'])+','+str(i['long']), i['violation_date']])

        print("Pending Violations has been saved to pending/", filename)
except:
    print("Failed in writing pending violations!!!!!")
input('Press any key to exit!!')
exit()
