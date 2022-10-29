from upload_api_01 import *

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
    display_img = input("\tInput Image Name (Name with Extension):")
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
    }
    tett.append(temp)

print("\nTimer Started!!")
x = time.perf_counter()
print("Processing Please Wait.............")
upload_dataset(tett)
print("Processing Complete.")
print("\nResult Summary:")
print("\tTotal Violations: ", len(tett))
print("\tTime Consume in Sec: ", time.perf_counter() - x)
print("\tGoogle Requests: ", get_google_count())
