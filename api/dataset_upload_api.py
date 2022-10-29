import requests
import math
import mysql.connector
import json

api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"

def db_connection():
    host = 'localhost'
    user = "root"
    password = ""
    database = 'elm'
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
    return cnx


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


def make_sec_point(lat1, lng1, lat2, lng2,):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+lat1+","+lng1+"&destination="+lat2+","+lng2+"&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    re = []
    if len(response.json()['routes'][0]['legs'][0]['steps']) == 1:
        print("Google Map: ",response.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value'],", ","Calculated: ",calcCrow(float(lat1), float(lng1), float(lat2), float(lng2)))
        if abs(calcCrow(float(lat1), float(lng1), float(lat2), float(lng2)) - float(response.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value'])) <= 0.6:
            re = [
                                {
                                    "lat":float(lat1),
                                    "lng": float(lng1),
                                },{
                                    "lat": float(lat2),
                                    "lng": float(lng2),
                                },
                        ]
    return re

def get_second_latlng_for_single_violation_by_direction_api(lat, long):
    full = 0.000400
    half = 0.000200
    qart = 0.000100
    l = [
        [
            lat + qart,
            long + full
        ], [
            lat - qart,
            long + full
        ], [
            lat + full,
            long + qart
        ], [
            lat + full,
            long - qart
        ],
        [
            lat - full,
            long + qart
        ], [
            lat - full,
            long - qart
        ], [
            lat - qart,
            long - full
        ], [
            lat + qart,
            long - full
        ],[
            lat + half,
            long + full
        ],[
            lat - half,
            long + full
        ],[
            lat + full,
            long + half
        ],[
            lat + full,
            long - half
        ],
        [
            lat - full,
            long + half
        ],[
            lat - full,
            long - half
        ],[
            lat - half,
            long - full
        ],[
            lat + half,
            long - full
        ],[
            lat - full,
            long - full
        ],[
            lat + full,
            long + full
        ],[
            lat - full,
            long + full
        ],[
            lat + full,
            long - full
        ],
        [
            lat - full,
            long
        ],
        [
            lat + full,
            long
        ],
        [
            lat,
            long - full
        ],
        [
            lat,
            long + full
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
    re = []
    for i in l:
        temp = make_sec_point(str(lat), str(long), str(i[0]), str(i[1]))
        if len(temp) > 0:
            re = temp
            break
        temp = make_sec_point(str(i[0]), str(i[1]), str(lat), str(long))
        if len(temp) > 0:
            re = temp
            break
    return re


def get_street_name(lat, long):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat)+","+str(long) + "&destination=" + str(lat)+","+str(long+0.000005) +  "&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("on")
    if len(temp1) > 1:
        v = temp1[1].split("</b>")[0].split("<b>")[1]
        if len(v.split("span")) > 1:
            v = v.split(">")[1].split("<")[0]

        return v
    else:
        temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("toward")
        if len(temp1) > 1:
            v = temp1[1].split("</b>")[0].split("<b>")[1]
            if len(v.split("span")) > 1:
                v = v.split(">")[1].split("<")[0]

            return v
        else:
            return get_street_name_second_try(lat, long)


def get_street_name_second_try(lat, long):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat)+","+str(long) + "&destination=" + str(lat+0.000005)+","+str(long+0.000005) +  "&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("on")
    if len(temp1) > 1:
        v = temp1[1].split("</b>")[0].split("<b>")[1]
        if len(v.split("span")) > 1:
            v = v.split(">")[1].split("<")[0]

        return v
    else:
        temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("toward")
        if len(temp1) > 1:
            v = temp1[1].split("</b>")[0].split("<b>")[1]
            if len(v.split("span")) > 1:
                v = v.split(">")[1].split("<")[0]

            return v
        else:
            return get_street_name_geocode(lat, long)


def get_street_name_geocode(lat, long):
    api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(long)+"&key=" + api_text

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    text = "\n"
    temp = 1
    for i in response['results']:
        for j in i['address_components']:
            for k in j['types']:
                if k == 'route':

                    return j['long_name']

    return "Unknown road"


def upload_new_street_name(name):
    cnx = db_connection()
    cursor = cnx.cursor()
    print(name)
    query = (
        "INSERT INTO `street`(`streetname`) VALUES ('"+name+"');")
    cursor.execute(query)
    cnx.commit()

    cursor_ = cnx.cursor()
    query = (
        "SELECT `streetid`  FROM `street` WHERE `streetname` = '"+name+"';")
    cursor_.execute(query)
    st_id = 0
    for a in cursor_:
        st_id = a
    cursor_.close()
    cnx.close()
    return st_id


def get_list_of_all_violations():
    all_list = []
    cnx = db_connection()
    cursor_ = cnx.cursor()
    query = (
        "SELECT `violationtypeid`, `violationname` FROM `violation_type` WHERE 1;")
    cursor_.execute(query)
    for a, b in cursor_:
        all_list.append({
            'violationtypeid': a,
            'violationname': b
        })
    cursor_.close()
    cnx.close()
    return all_list


def get_distance_btw_violation_by_distance_matrix_api(lat1, lng1, lat2, lng2):
    url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat1) + "," + str(lng1) + "&destination=" + str(lat2) + "," + str(lng2) + "&mode=walking&key=" + api_text
    response1 = requests.request("GET", url1, headers={}, data={})
    one = response1.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value']

    if len(response1.json()['routes'][0]['legs'][0]['steps']) == 1:
        return True
    else:
        return False


def upload_dataset(dataset):
    set_of_street_names = set()
    list_of_street_names = []
    list_of_violations = get_list_of_all_violations()
    final_list_of_data = []

    # get street names of all rows
    for j in range(len(dataset)):
        temp_name = get_street_name(dataset[j]['lat'], dataset[j]['long'])
        dataset[j]['street_name'] = temp_name
        set_of_street_names.add(temp_name)

    # Get Street Ids from Database and add street id with street name
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
        "SELECT `streetid`, `streetname` FROM `street` ORDER BY `streetid` ASC;")
    cursor.execute(query)
    to_remove_set = set()
    for a, b in cursor:
        for i in set_of_street_names:
            if i == b:
                temp = []
                for j in range(len(dataset)):
                    if dataset[j]['street_name'] == i:
                        dataset[j]['street_id'] = a
                        for mk in list_of_violations:
                            if dataset[j]['violation'] == mk['violationname']:
                                dataset[j]['violation_type_id'] = mk['violationtypeid']
                        temp.append(dataset[j])
                list_of_street_names.append({"street_id": a, "street_name": b, "violation": temp})
                to_remove_set.add(i)
                break
    for i in to_remove_set:
        set_of_street_names.remove(i)
    cursor.close()
    cnx.close()

    for i in set_of_street_names:
        st_id = upload_new_street_name(i)
        temp = []
        for j in range(len(dataset)):
            if dataset[j]['street_name'] == i:
                dataset[j]['street_id'] = st_id
                for mk in list_of_violations:
                    if dataset[j]['violation'] == mk['violationname']:
                        dataset[j]['violation_type_id'] = mk['violationtypeid']
                temp.append(dataset[j])
        list_of_street_names.append({"street_id": st_id, "street_name": i, "violation": temp})
        #set_of_street_names.remove(i)

    print(list_of_street_names)
    # Sort and Separate rows by turns of single road
    for street in list_of_street_names:
        if len(street['violation']) > 1:
            point_one = []
            point_two = []
            point_one.append(street['violation'][0])
            for violation in range(1, len(street['violation'])):
                if get_distance_btw_violation_by_distance_matrix_api(street['violation'][0]['lat'],street['violation'][0]['long'],street['violation'][violation]['lat'],street['violation'][violation]['long']):
                    point_one.append(street['violation'][violation])
                else:
                    point_two.append(street['violation'][violation])
            if len(point_one) > 1:
                max_distance = 0
                max_distance_point_01 = 0
                max_distance_point_02 = 0
                for violation in range(len(point_one)):
                    for sec_vio in range(len(point_one)):
                        if violation == sec_vio:
                            continue
                        dist = calcCrow(point_one[violation]['lat'],point_one[violation]['long'],point_one[sec_vio]['lat'],point_one[sec_vio]['long'])
                        if max_distance < dist:
                            max_distance = dist
                            max_distance_point_01 = violation
                            max_distance_point_02 = sec_vio
                if max_distance <= 300:
                    point_one[max_distance_point_01]['start_latlng'] = str(point_one[max_distance_point_01]['lat'])+","+str(point_one[max_distance_point_01]['long'])
                    point_one[max_distance_point_01]['end_latlng'] = str(point_one[max_distance_point_02]['lat'])+","+str(point_one[max_distance_point_02]['long'])
                else:
                    sorted_points = []
                    sorted_points.append(max_distance_point_01)
                    for count in range(len(point_one)-1):
                        min_dis = 1000000000000000
                        min_dist_point = 0
                        for violation in range(len(point_one)):
                            if violation == max_distance_point_01 or violation in sorted_points:
                                continue
                            dist = calcCrow(point_one[violation]['lat'], point_one[violation]['long'],
                                            point_one[max_distance_point_01]['lat'], point_one[max_distance_point_01]['long'])
                            if min_dis > dist:
                                min_dis = dist
                                min_dist_point = violation

                        sorted_points.append(min_dist_point)
                    start_point = 0
                    last_point = -1
                    point = 0
                    while point < len(sorted_points) - 1:
                        dist = calcCrow(point_one[sorted_points[point]]['lat'], point_one[sorted_points[point]]['long'],
                                        point_one[sorted_points[point+1]]['lat'],
                                        point_one[sorted_points[point+1]]['long'])
                        if dist <= 300:
                            last_point = point + 1
                        else:
                            if last_point == -1:
                                got_sec = get_second_latlng_for_single_violation_by_direction_api(point_one[sorted_points[start_point]]['lat'],point_one[sorted_points[start_point]]['long'])
                                if len(got_sec) == 2:
                                    point_one[sorted_points[start_point]]['start_latlng'] = str(got_sec[0]['lat']
                                        ) + "," + str(got_sec[0]['lng'])
                                    point_one[sorted_points[start_point]]['end_latlng'] = str(got_sec[1]['lat']) + "," + str(
                                        got_sec[1]['lng'])
                                else:
                                    point_one[sorted_points[start_point]]['start_latlng'] = str(point_one[sorted_points[start_point]]['lat']
                                                                                                ) + "," + str(
                                        point_one[sorted_points[start_point]]['long'])
                                    point_one[sorted_points[start_point]]['end_latlng'] = "0"
                                start_point = start_point + 1
                            else:
                                point_one[sorted_points[start_point]]['start_latlng'] = str(
                                    point_one[sorted_points[start_point]]['lat']) + "," + str(
                                    point_one[sorted_points[start_point]]['long'])
                                point_one[sorted_points[start_point]]['end_latlng'] = str(
                                    point_one[sorted_points[last_point]]['lat']) + "," + str(
                                    point_one[sorted_points[last_point]]['long'])
                                start_point = last_point + 1
                                last_point = -1
                        point = point + 1
                for i in point_one:
                    final_list_of_data.append(i)
            else:
                # point_one[0]['start_latlng'] = str(point_one[0]['lat'])+","+str(point_one[0]['long'])
                # point_one[0]['end_latlng'] = "0"
                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                    point_one[0]['lat'], point_one[0]['long'])
                if len(got_sec) == 2:
                    point_one[0]['start_latlng'] = str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng'])
                    point_one[0]['end_latlng'] = str(got_sec[1]['lat']) + "," + str(
                        got_sec[1]['lng'])
                else:
                    point_one[0]['start_latlng'] = str(point_one[0]['lat'])+","+str(point_one[0]['long'])
                    point_one[0]['end_latlng'] = "0"
                final_list_of_data.append(point_one[0])

            if len(point_two) > 1:
                max_distance = 0
                max_distance_point_01 = 0
                max_distance_point_02 = 0
                for violation in range(len(point_two)):
                    for sec_vio in range(len(point_two)):
                        if violation == sec_vio:
                            continue
                        dist = calcCrow(point_two[violation]['lat'], point_two[violation]['long'],
                                        point_two[sec_vio]['lat'],
                                        point_two[sec_vio]['long'])
                        if max_distance < dist:
                            max_distance = dist
                            max_distance_point_01 = violation
                            max_distance_point_02 = sec_vio
                if max_distance <= 300:
                    point_two[max_distance_point_01]['start_latlng'] = str(
                        point_two[max_distance_point_01]['lat']) + "," + str(
                        point_two[max_distance_point_01]['long'])
                    point_two[max_distance_point_01]['end_latlng'] = str(
                        point_two[max_distance_point_02]['lat']) + "," + str(
                        point_two[max_distance_point_02]['long'])
                else:
                    sorted_points = []
                    sorted_points.append(max_distance_point_01)
                    for count in range(len(point_two) - 1):
                        min_dis = 1000000000000000
                        min_dist_point = 0
                        for violation in range(len(point_two)):
                            if violation == max_distance_point_01 or violation in sorted_points:
                                continue
                            dist = calcCrow(point_two[violation]['lat'], point_two[violation]['long'],
                                            point_two[max_distance_point_01]['lat'],
                                            point_two[max_distance_point_01]['long'])
                            if min_dis > dist:
                                min_dis = dist
                                min_dist_point = violation

                        sorted_points.append(min_dist_point)
                    start_point = 0
                    last_point = -1
                    point = 0
                    while point < len(sorted_points) - 1:
                        dist = calcCrow(point_two[sorted_points[point]]['lat'], point_two[sorted_points[point]]['long'],
                                        point_two[sorted_points[point + 1]]['lat'],
                                        point_two[sorted_points[point + 1]]['long'])
                        if dist <= 300:
                            last_point = point + 1
                        else:
                            if last_point == -1:
                                # point_two[sorted_points[start_point]]['start_latlng'] = str(
                                #     point_two[sorted_points[start_point]]['lat']) + "," + str(
                                #     point_two[sorted_points[start_point]]['long'])
                                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                                    point_two[sorted_points[start_point]]['lat'],
                                    point_two[sorted_points[start_point]]['long'])
                                if len(got_sec) == 2:
                                    point_two[sorted_points[start_point]]['start_latlng'] = str(got_sec[0]['lat']
                                                                                                ) + "," + str(
                                        got_sec[0]['lng'])
                                    point_two[sorted_points[start_point]]['end_latlng'] = str(
                                        got_sec[1]['lat']) + "," + str(
                                        got_sec[1]['lng'])
                                else:
                                    point_two[sorted_points[start_point]]['start_latlng'] = str(
                                        point_two[sorted_points[start_point]]['lat']) + "," + str(
                                        point_two[sorted_points[start_point]]['long'])
                                start_point = start_point + 1
                            else:
                                point_two[sorted_points[start_point]]['start_latlng'] = str(
                                    point_two[sorted_points[start_point]]['lat']) + "," + str(
                                    point_two[sorted_points[start_point]]['long'])
                                point_two[sorted_points[start_point]]['end_latlng'] = str(
                                    point_two[sorted_points[last_point]]['lat']) + "," + str(
                                    point_two[sorted_points[last_point]]['long'])
                                start_point = last_point + 1
                                last_point = -1
                        point = point + 1
                for i in point_two:
                    final_list_of_data.append(i)
                # else:
                #     point_two[0]['start_latlng'] = str(point_two[0]['lat']) + "," + str(point_two[0]['long'])
                #     point_two[0]['end_latlng'] = "0"
                # final_list_of_data.append(point_two[0])

            elif len(point_two) == 1:
                # point_two[0]['start_latlng'] = str(point_two[0]['lat'])+","+str(point_two[0]['long'])
                # point_two[0]['end_latlng'] = "0"
                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                    point_two[0]['lat'], point_two[0]['long'])
                if len(got_sec) == 2:
                    point_two[0]['start_latlng'] = str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng'])
                    point_two[0]['end_latlng'] = str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng'])
                else:
                    point_two[0]['start_latlng'] = str(point_two[0]['lat'])+","+str(point_two[0]['long'])
                    point_two[0]['end_latlng'] = "0"
                final_list_of_data.append(point_two[0])
        else:
            # street['violation'][0]['start_latlng'] = str(street['violation'][0]['lat']) + "," + str(street['violation'][0]['long'])
            # street['violation'][0]['end_latlng'] = "0"
            got_sec = get_second_latlng_for_single_violation_by_direction_api(
                street['violation'][0]['lat'], street['violation'][0]['long'])
            if len(got_sec) == 2:
                street['violation'][0]['start_latlng'] = str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng'])
                street['violation'][0]['end_latlng'] = str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng'])
            else:
                street['violation'][0]['start_latlng'] = str(street['violation'][0]['lat']) + "," + str(street['violation'][0]['long'])
                street['violation'][0]['end_latlng'] = "0"
            final_list_of_data.append(street['violation'][0])
    for vio in final_list_of_data:
        if vio['start_latlng'] != '0' and vio['end_latlng'] != '0':
            pass

    reminder = int(len(final_list_of_data) % 10)
    whole_num = int((len(final_list_of_data) - reminder) / 10)

    for i in range(whole_num):
        query_data_list = []
        for j in range(i*10, i*10+10):
            query_data_list.append("('"+str(final_list_of_data[j]['street_id'])+"','"+str(final_list_of_data[j]['violation_type_id'])+"','"+str(final_list_of_data[j]['details'])+"','"+str(final_list_of_data[j]['accurate'])+"','"+str(final_list_of_data[j]['risk'])+"','"+str(final_list_of_data[j]['display_img'])+"','"+str(final_list_of_data[j]['lat'])+"','"+str(final_list_of_data[j]['long'])+"','"+str(final_list_of_data[j]['start_latlng'])+"','"+str(final_list_of_data[j]['end_latlng'])+"','"+str(final_list_of_data[j]['violation_date'])+"','2022-10-28 "+str(final_list_of_data[j]['violation_time'])+"','0','0','0')")

        query = query_data_list[0]
        for j in range(1, 10):
            query = query + ","+query_data_list[j]

        x = requests.post('http://127.0.0.1:1151/insertviolationdata', json={"query": query})
        print(x.text)

    query_data_list = []
    for j in range(whole_num*10, whole_num*10 + reminder):
        query_data_list.append("('"+str(final_list_of_data[j]['street_id'])+"','"+str(final_list_of_data[j]['violation_type_id'])+"','"+str(final_list_of_data[j]['details'])+"','"+str(final_list_of_data[j]['accurate'])+"','"+str(final_list_of_data[j]['risk'])+"','"+str(final_list_of_data[j]['display_img'])+"','"+str(final_list_of_data[j]['lat'])+"','"+str(final_list_of_data[j]['long'])+"','"+str(final_list_of_data[j]['start_latlng'])+"','"+str(final_list_of_data[j]['end_latlng'])+"','"+str(final_list_of_data[j]['violation_date'])+"','2022-10-28 "+str(final_list_of_data[j]['violation_time'])+"','0','0','0')")

    query = query_data_list[0]
    for j in range(1, len(query_data_list)):
        query = query + "," + query_data_list[j]
    x = requests.post('http://127.0.0.1:1151/insertviolationdata', json={"query": query})
    print(x.text)

tett  = [
    {
    "lat":24.62503,
    "long":46.70920,
    "violation":"Rubble Source",
    "details":"Rubble Source",
    "accurate":95,
    "risk":2,
    "display_img":"1.jpg",
    "violation_date":"2022-10-08",
    "violation_time":"14:29",
    "device_id":0,
    "polygon_img":"",

    "street_id":0,
    "street_name":"",
    "violation_type_id":0,



    "start_latlng":0,
    "end_latlng":0,

    },
{
    "lat": 24.62488,
    "long": 46.70893,
    "violation": "Major Asphalt",
    "details": "Major Asphalt",
    "accurate": 7,
    "risk": 6,
    "display_img": "2.jpg",
    "violation_date": "2022-10-08",
    "violation_time": "14:30",

    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.64750,
    "long": 46.70259,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "3.jpg",
    "violation_time": "14:13",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },

{
    "lat": 24.67188,
    "long": 46.69218,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "5.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },

{
    "lat": 24.67152,
    "long": 46.69241,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "7.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },

{
    "lat": 24.67134,
    "long": 46.69253,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "9.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.68044,
    "long": 46.68813,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "10.jpg",
    "violation_time": "14:10",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.66005,
    "long": 46.70085,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "10.jpg",
    "violation_time": "14:12",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.67117,
    "long": 46.69265,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "12.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.70544,
    "long": 46.67516,
    "violation": "Street Sweeping",
    "details": "Street Sweeping",
    "accurate": 95,
    "risk": 2,
    "display_img": "13.jpg",
    "violation_time": "14:05",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.67100,
    "long": 46.69278,
    "violation": "Street Sweeping",
    "details": "Street Sweeping",
    "accurate": 95,
    "risk": 2,
    "display_img": "14.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.63044,
    "long": 46.71588,
    "violation": "Median",
    "details": "Median",
    "accurate": 95,
    "risk": 2,
    "display_img": "15.jpg",
    "violation_time": "14:18",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.67083,
    "long": 46.69293,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "16.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.65959,
    "long": 46.70091,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "17.jpg",
    "violation_time": "14:12",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.67066,
    "long": 46.69307,
    "violation": "Street Sweeping",
    "details": "Street Sweeping",
    "accurate": 95,
    "risk": 2,
    "display_img": "18.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
{
    "lat": 24.63015,
    "long": 46.71597,
    "violation": "Median",
    "details": "Median",
    "accurate": 95,
    "risk": 2,
    "display_img": "21.jpg",
    "violation_time": "14:18",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
    },
{
    "lat": 24.67032,
    "long": 46.69339,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "22.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
    },
{
    "lat": 24.67032,
    "long": 46.69339,
    "violation": "Street Sweeping",
    "details": "Street Sweeping",
    "accurate": 95,
    "risk": 2,
    "display_img": "23.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
    {
    "lat": 24.63196,
    "long": 46.71576,
    "violation": "Median",
    "details": "Median",
    "accurate": 95,
    "risk": 2,
    "display_img": "24.jpg",
    "violation_time": "14:28",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
    },
{
    "lat": 24.67000,
    "long": 46.69373,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "25.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
    },
{
    "lat": 24.66984,
    "long": 46.69391,
    "violation": "Street Sweeping",
    "details": "Street Sweeping",
    "accurate": 95,
    "risk": 2,
    "display_img": "26.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,

    },
    {
        "lat": 24.63184,
        "long": 46.71580,
        "violation": "Median",
        "details": "Median",
        "accurate": 95,
        "risk": 2,
        "display_img": "27.jpg",
        "violation_time": "14:28",

        "violation_date": "2022-10-08",
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
    "lat": 24.66968,
    "long": 46.69409,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "28.jpg",
    "violation_time": "14:11",

    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
    },
    {
        "lat": 24.63173,
        "long": 46.71584,
        "violation": "Median",
        "details": "Median",
        "accurate": 95,
        "risk": 2,
        "display_img": "29.jpg",
        "violation_time": "14:28",

        "violation_date": "2022-10-08",
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.66968,
        "long": 46.69409,
        "violation": "Street Sweeping",
        "details": "Street Sweeping",
        "display_img": "30.jpg",
        "violation_time": "14:11",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.63161,
        "long": 46.71588,
        "violation": "Median",
        "details": "Median",
        "display_img": "31.jpg",
        "violation_time": "14:28",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.64381,
        "long": 46.70303,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "32.jpg",
        "violation_time": "14:13",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.70086,
        "long": 46.67760,
        "violation": "Street Sweeping",
        "details": "Street Sweeping",
        "display_img": "33.jpg",
        "violation_time": "14:06",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.64324,
        "long": 46.70308,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "34.jpg",
        "violation_time": "14:13",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.64306,
        "long": 46.70310,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "35.jpg",
        "violation_time": "14:13",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.62704,
        "long": 46.71216,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "36.jpg",
        "violation_time": "14:29",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.64289,
        "long": 46.70312,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "37.jpg",
        "violation_time": "14:13",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.62704,
        "long": 46.71216,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "38.jpg",
        "violation_time": "14:29",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.64273,
        "long": 46.70314,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "39.jpg",
        "violation_time": "14:13",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.62679,
        "long": 46.71179,
        "violation": "Major Asphalt",
        "details": "Major Asphalt",
        "display_img": "40.jpg",
        "violation_time": "14:29",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.64220,
        "long": 46.70319,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "41.jpg",
        "violation_time": "14:13",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.62667,
        "long": 46.71159,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "42.jpg",
        "violation_time": "14:29",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.70381,
        "long": 46.67597,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "43.jpg",
        "violation_time": "14:05",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.62819,
        "long": 46.70886,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "44.jpg",
        "violation_time": "14:23",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.65328,
        "long": 46.70177,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "45.jpg",
        "violation_time": "14:12",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.63427,
        "long": 46.70392,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "46.jpg",
        "violation_time": "14:14",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.62507,
        "long": 46.70926,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "47.jpg",
        "violation_time": "14:19",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.63024,
        "long": 46.70724,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "48.jpg",
        "violation_time": "14:25",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },

{
        "lat": 24.70680,
        "long": 46.67471,
        "violation": "Communication Tower",
        "details": "Communication Tower",
        "display_img": "49.jpg",
        "violation_time": "14:04",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.67365,
        "long": 46.69122,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "50.jpg",
        "violation_time": "14:11",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.63150,
        "long": 46.70430,
        "violation": "Street Sweeping",
        "details": "Street Sweeping",
        "display_img": "51.jpg",
        "violation_time": "14:15",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.69054,
        "long": 46.68283,
        "violation": "Major Asphalt",
        "details": "Major Asphalt",
        "display_img": "52.jpg",
        "violation_time": "14:09",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.63144,
        "long": 46.70430,
        "violation": "Street Sweeping",
        "details": " Street Sweeping",
        "display_img": "54.jpg",
        "violation_time": "14:15",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.67348,
        "long": 46.69132,
        "violation": "Rubble Source",
        "details": " Rubble Source",
        "display_img": "55.jpg",
        "violation_time": "14:11",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.67330,
        "long": 46.69141,
        "violation": "Rubble Source",
        "details": " Rubble Source",
        "display_img": "56.jpg",
        "violation_time": "14:11",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.67312,
        "long": 46.69151,
        "violation": "Rubble Source",
        "details": " Rubble Source",
        "display_img": "57.jpg",
        "violation_time": "14:11",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
{
        "lat": 24.62819,
        "long": 46.70897,
        "violation": "Minor Asphalt",
        "details": " Minor Asphalt",
        "display_img": "58.jpg",
        "violation_time": "14:23",

        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
    },
]

upload_dataset(tett)
# Street Sweeping
# Median
# Rubble Source
# Major Asphalt
# Minor Asphalt
# Communication Tower