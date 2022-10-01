import requests
import math
api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"


def to_rad(v):
    return v * math.pi / 180

def calcCrow(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = to_rad(lat2-lat1)
    dLon = to_rad(lon2-lon1)
    lat1 = to_rad(lat1)
    lat2 = to_rad(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d*1000


def get_street_name(lat, long):
    api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+long+"&key=" + api_text

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    for i in response['results']:
        for j in i['address_components']:
            print(j)
            for k in j['types']:
                if k == 'route':
                    print(j['long_name'])


def make_sec_point(start_latlng, end_latlng):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+start_latlng+"&destination="+end_latlng+"&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    print(response.json()['routes'][0]['legs'][0]['steps'])
    print(len(response.json()['routes'][0]['legs'][0]['steps']))


lat = []
long = []
name = []
#Tebbeen
name.append("Tebbeen")
lat.append('21.496987')
long.append('39.188711')

# for i in range(len(lat)):
#     get_street_name(lat[i], long[i])

# #lat -200
# make_sec_point("21.497921,39.187487", "21.497721,39.187487")
# make_sec_point("21.497721,39.187487", "21.497921,39.187487")
#
# #lat +200
# make_sec_point("21.498121,39.187487", "21.497921,39.187487")
# make_sec_point("21.497921,39.187487", "21.498121,39.187487")
#
# #lng -200
# make_sec_point("21.497921,39.187487", "21.497921,39.187287")
# make_sec_point("21.497921,39.187287", "21.497921,39.187487")
#
# #lng +200
# make_sec_point("21.497921,39.187487", "21.497921,39.187687")
# make_sec_point("21.497921,39.187687", "21.497921,39.187487" )


latlng = [21.494113, 39.204321]

make_sec_point(str(21.496987)+","+str(39.188711), str(21.496987-0.00001)+","+str(39.188711))

#lat -200
print("for: ", str(latlng[0]-0.000300)+","+str(latlng[1]))
make_sec_point(str(latlng[0])+","+str(latlng[1]), str(latlng[0]-0.000300)+","+str(latlng[1]))
print(calcCrow(latlng[0], latlng[1], latlng[0]-0.000300, latlng[1]))
make_sec_point(str(latlng[0]-0.000300)+","+str(latlng[1]), str(latlng[0])+","+str(latlng[1]))
print(calcCrow(latlng[0]-0.000300, latlng[1], latlng[0], latlng[1]))

#lat +200
print("for: ", str(latlng[0]+0.000300)+","+str(latlng[1]))
make_sec_point(str(latlng[0])+","+str(latlng[1]), str(latlng[0]+0.000300)+","+str(latlng[1]))
print(calcCrow(latlng[0], latlng[1], latlng[0]+0.000300, latlng[1]))
make_sec_point(str(latlng[0]+0.000300)+","+str(latlng[1]), str(latlng[0])+","+str(latlng[1]))
print(calcCrow(latlng[0]+0.000300, latlng[1], latlng[0], latlng[1]))

#lng -200
print("for: ", str(latlng[0])+","+str(latlng[1]-0.000300))
make_sec_point(str(latlng[0])+","+str(latlng[1]), str(latlng[0])+","+str(latlng[1]-0.000300))
print(calcCrow(latlng[0], latlng[1], latlng[0], latlng[1]-0.000300))
make_sec_point(str(latlng[0])+","+str(latlng[1]-0.000300), str(latlng[0])+","+str(latlng[1]))
print(calcCrow(latlng[0], latlng[1]-0.000300, latlng[0], latlng[1]))

#lng +200
print("for: ", str(latlng[0])+","+str(latlng[1]+0.000300))
make_sec_point(str(latlng[0])+","+str(latlng[1]), str(latlng[0])+","+str(latlng[1]+0.000300))
print(calcCrow(latlng[0], latlng[1], latlng[0], latlng[1]+0.000300))
make_sec_point(str(latlng[0])+","+str(latlng[1]+0.000300), str(latlng[0])+","+str(latlng[1]))
print(calcCrow(latlng[0], latlng[1]+0.000300, latlng[0], latlng[1]))



