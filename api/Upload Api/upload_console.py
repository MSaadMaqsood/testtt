import time
import cv2
import base64
import requests
from requests import request

i = 0

i = int(input("Enter amount of Violations: "))
tett = []
for vio in range(i):
    print("Violation ", vio+1, ": ")
    latlng = input("\tInput Lat Long ( lat,long ): ")
    print("\tInput Violation Type:")
    print("\t\t1. Minor Asphalt  2.Sidewalk  3.Lighting  4.Cleanliness  5. Afforestation")
    print("\t\t6. Fossils  7. Major Asphalt  8. Rubble Source  9. Street Sweeping  ")
    print("\t\t10.  Median  11. Communication Tower")

    violation = int(input("\tInput Violation Index: "))
    details = (input("\tInput Details: "))
    accurate = int(input("\tInput Accuracy (Number 00 - 100): "))
    risk = int(input("\tInput Risk (Number 00 - 100): "))
    display_img = input("\tInput Image Name (Name with Extension .jpg):")
    device_id = int(input("\tInput Device ID:"))
    polygon_img = input("\tInput Polygon Coordinates :")
    vio = ""
    if violation == 1:
        vio = "Minor Asphalt"
    if violation == 2:
        vio = "Sidewalk"
    if violation == 3:
        vio = "Lighting"
    if violation == 4:
        vio = "Cleanliness"
    if violation == 5:
        vio = "Afforestation"
    if violation == 6:
        vio = "Fossils"
    if violation == 7:
        vio = "Major Asphalt"
    if violation == 8:
        vio = "Rubble Source"
    if violation == 9:
        vio = "Street Sweeping"
    if violation == 10:
        vio = "Median"
    if violation == 11:
        vio = "Communication Tower"

    img = cv2.imread('to_upload_img/'+display_img)
    string_img = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    temp = {

        "lat": float(latlng.split(',')[0]),
        "long": float(latlng.split(',')[1]),
        "violation": vio,
        "details": details,
        "accurate": accurate,
        "risk": risk,
        "display_img": display_img,
        "violation_date": "2022-10-08",
        "violation_time": "14:29",

        "device_id": device_id,
        "polygon_img": polygon_img,

        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,

        "string_img": string_img
    }
    tett.append(temp)

print("\nTimer Started!!")
x = time.perf_counter()
print("Processing Please Wait.............")
#pending = upload_dataset(tett)
re = requests.post("http://127.0.0.1:1255/upload_vio", json={'vio' : tett})
print(re)
pending = re.json()['pending']

print("Processing Complete.")
print("\nResult Summary:")
print("\tTotal Violations: ", len(tett))
print("\tTime Consume in Sec: ", time.perf_counter() - x)
print("\tBusy Streets: ", len(pending))


while len(pending) != 0:

    print("Waiting for Streets to Free (retry after 2min).")
    time.sleep(120)
    print("\nRetry Timer Started!!")
    x = time.perf_counter()
    print("Processing Please Wait.............")
    #pending = retry_upload_dataset(pending)
    re = requests.post("http://127.0.0.1:1255/retry_upload_vio", json={'vio': pending})
    pending = re.json()['pending']
    print("Processing Complete.")
    print("\nResult Summary:")
    print("\tTime Consume in Sec: ", time.perf_counter() - x)
    print("\tBusy Streets: ", len(pending))
