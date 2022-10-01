import requests
import math

api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"


def to_rad(v):
    return v * math.pi / 180


def calcCrow(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = to_rad(lat2 - lat1)
    dLon = to_rad(lon2 - lon1)
    lat1 = to_rad(lat1)
    lat2 = to_rad(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000


def make_sec_point(lat1, lng1, lat2, lng2):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + lat1 + "," + lng1 + "&destination=" + lat2 + "," + lng2 + "&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    re = False
    if len(response.json()['routes'][0]['legs'][0]['steps']) == 1:
        print("Google Map: ", response.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value'], ", ",
              "Calculated: ", calcCrow(float(lat1), float(lng1), float(lat2), float(lng2)))
        if int(calcCrow(float(lat1), float(lng1), float(lat2), float(lng2))) == \
                response.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value']:
            re = True
    return re


def get_street_name(lat, long):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat) + "," + str(
        long) + "&destination=" + str(lat) + "," + str(long + 0.000005) + "&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("on")
    if len(temp1) > 1:
        v = temp1[1].split("</b>")[0].split("<b>")[1]
        return v
    else:
        temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("toward")
        if len(temp1) > 1:
            v = temp1[1].split("</b>")[0].split("<b>")[1]
            return v
        else:
            return get_street_name_second_try(lat, long)

    # print(response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("<b>")[2].split("</b>")[0])
    # print(response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'])
    # print(response.json()['routes'][0]['legs'][0])


def get_street_name_second_try(lat, long):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat) + "," + str(
        long) + "&destination=" + str(lat + 0.000005) + "," + str(long + 0.000005) + "&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("on")
    if len(temp1) > 1:
        v = temp1[1].split("</b>")[0].split("<b>")[1]
        return v
    else:
        temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("toward")
        if len(temp1) > 1:
            v = temp1[1].split("</b>")[0].split("<b>")[1]
            return v
        else:
            return "Unknown road" + " \" " + response.json()['routes'][0]['legs'][0]['steps'][0][
                'html_instructions'] + " \""


def get_street_name_geocode(lat, long):
    api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(long) + "&key=" + api_text

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    text = "\n"
    temp = 1
    for i in response['results']:
        for j in i['address_components']:
            for k in j['types']:
                if k == 'route':
                    text = text + "\t" + str(temp) + ". " + j['long_name'] + "\n"
                    temp = temp + 1
    return text


def get_distance_btw_violation_by_direction_api(lat1, lng1, lat2, lng2):
    url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat1) + "," + str(lng1) + "&destination=" + str(lat2) + "," + str(lng2) + "&key=" + api_text
    response1 = requests.request("GET", url1, headers={}, data={})
    one = response1.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value']

    url2 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat2) + "," + str(
        lng2) + "&destination=" + str(lat1) + "," + str(lng1) + "&key=" + api_text
    response2 = requests.request("GET", url2, headers={}, data={})
    two = response2.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value']
    print(one)
    print(two)
    if one <= two:
        if len(response1.json()['routes'][0]['legs'][0]['steps']) ==1:
            return one
        else:
            return 0
    else:
        if len(response2.json()['routes'][0]['legs'][0]['steps']) ==1:
            return two
        else:
            return 0


def get_distance_btw_violation_by_distance_matrix_api(lat1, lng1, lat2, lng2):
    url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(lat1) + "," + str(
        lng1) + "&destinations=" + str(lat2) + "," + str(lng2) + "&key=" + api_text
    response1 = requests.request("GET", url1, headers={}, data={})
    print(response1.text)

    url2 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(lat2) + "," + str(
        lng2) + "&destinations=" + str(lat1) + "," + str(lng1) + "&key=" + api_text
    response2 = requests.request("GET", url2, headers={}, data={})
    print(response2.text)


def get_second_latlng_for_single_violation_by_direction_api(lat, long):
    l = [
        [
            lat - 0.000300,
            long
        ],
        [
            lat + 0.000300,
            long
        ],
        [
            lat,
            long - 0.000300
        ],
        [
            lat,
            long + 0.000300
        ],
        [
            lat - 0.000300,
            long - 0.000300
        ], [
            lat + 0.000300,
            long + 0.000300
        ], [
            lat - 0.000300,
            long + 0.000300
        ], [
            lat + 0.000300,
            long - 0.000300
        ], [
            lat + 0.000150,
            long + 0.000300
        ], [
            lat - 0.000150,
            long + 0.000300
        ], [
            lat + 0.000300,
            long + 0.000150
        ], [
            lat + 0.000300,
            long - 0.000150
        ],
        [
            lat - 0.000300,
            long + 0.000150
        ], [
            lat - 0.000300,
            long - 0.000150
        ], [
            lat - 0.000150,
            long - 0.000300
        ], [
            lat + 0.000150,
            long - 0.000300
        ],
    ]
    # lat -200
    # lat +200
    # lng -200
    # lng +200
    # lat -300 lng -300
    # lat +200 lng -300
    # lat -300 lng +300
    # lat +300 lng +300
    # lat +300 lng +150
    for i in l:
        print("for: ", str(i[0]) + "," + str(i[1]))
        if make_sec_point(str(lat), str(long), str(i[0]), str(i[1])):
            break
        if make_sec_point(str(i[0]), str(i[1]), str(lat), str(long)):
            break
        print("")


def test_get_street_name_by_direction_api():
    latlng = [
        [
            21.473241, 39.228311
        ],
        [
            21.479985, 39.212571
        ],
        [
            21.480736, 39.209832
        ],
        [
            21.478323, 39.209798
        ], [
            21.478012, 39.213322
        ]
    ]
    print("Testing Direction api")
    temp_count = 1
    for i in latlng:
        print(str(temp_count) + ". ", get_street_name(i[0], i[1]))
        temp_count = temp_count + 1


def test_get_street_name_by_geocode_api():
    latlng = [
        [
            21.473241, 39.228311
        ],
        [
            21.479985, 39.212571
        ],
        [
            21.480736, 39.209832
        ],
        [
            21.478323, 39.209798
        ], [
            21.478012, 39.213322
        ]
    ]
    print("Testing geocode api")
    temp_count = 1
    for i in latlng:
        print(str(temp_count) + ". ", get_street_name_geocode(i[0], i[1]))
        temp_count = temp_count + 1


def compare_get_street_name():
    latlng = [
        [
            21.473241, 39.228311
        ],
        [
            21.479985, 39.212571
        ],
        [
            21.480736, 39.209832
        ],
        [
            21.478323, 39.209798
        ],
        [
            21.478012, 39.213322
        ]
    ]
    print("Testing Direction api")
    temp_count = 1
    for i in latlng:
        print(str(temp_count) + ". ", get_street_name(i[0], i[1]))
        temp_count = temp_count + 1

    print("\nTesting geocode api")
    temp_count = 1
    for i in latlng:
        print(str(temp_count) + ". ", get_street_name_geocode(i[0], i[1]))
        temp_count = temp_count + 1


# compare_get_street_name()
# get_second_latlng_for_single_violation_by_direction_api(21.494544, 39.205980)
# print(get_distance_btw_violation_by_distance_matrix_api(21.603970, 39.190792,21.487862, 39.233131))


def violation_map_data():
    street_list = [1, 2]

    temp = [
        [
            {
                "id": 1,
                "street_id": 1,
                "lat": 21.548605,
                "long": 39.221821,
            }, {
            "id": 2,
            "street_id": 1,
            "lat": 21.550661,
            "long": 39.221493,
        }, {
            "id": 3,
            "street_id": 1,
            "lat": 21.551413,
            "long": 39.221327,
        }, {
            "id": 6,
            "street_id": 1,
            "lat": 21.554086,
            "long": 39.220643,
        }
        ],
        [
            {
                "id": 4,
                "street_id": 2,
                "lat": 21.550175,
                "long": 39.222608,
            }, {
            "id": 5,
            "street_id": 2,
            "lat": 21.550215,
            "long": 39.223380,
        },
        ]
    ]
    used = []
    for i in temp:
        ignore = []
        for j in i:
            make = False
            if j['id'] in ignore:
                continue
            for k in i:
                if j['id'] == k['id']:
                    continue
                dist = get_distance_btw_violation_by_distance_matrix_api(k['lat'], k['long'], j['lat'], j['long'])
                if dist < 150:
                    print(k['id'], dist)
                    ignore.append(k['id'])
                    used.append([
                        {
                            "street_id": k['street_id'],
                            "lat": k['lat'],
                            "lng": k['long'],
                        }, {
                            "street_id": k['street_id'],
                            "lat": j['lat'],
                            "lng": j['long'],
                        },
                    ]
                    )
                    make = True
            if not make:
                get_second_latlng_for_single_violation_by_direction_api(j['lat'], j['long'], j['street_id'])

    print(used)


get_distance_btw_violation_by_distance_matrix_api(21.550661,39.221493,21.551413,39.221327)
get_distance_btw_violation_by_direction_api(21.550661,39.221493,21.551413,39.221327)


