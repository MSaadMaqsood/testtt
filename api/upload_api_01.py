from datetime import datetime
import requests
import math
import mysql.connector
import json
import ast
import polyline
import time

api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"
google_request = 0
database_request = 0

def db_connection():
    host = '67.205.163.34'
    user = "sohail"
    password = "sohail123"
    database = 'elm1'
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


def make_responce_of_two_point(latlng1, latlng2):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+latlng1+"&destination="+latlng2+"&key=" + api_text

    response = requests.request("GET", url, headers={}, data={})
    global google_request
    google_request += 1
    l = polyline.decode(response.json()["routes"][0]['overview_polyline']['points'])
    al = []
    for i in l:
        temp = {'lat': i[0], 'lng': i[1]}
        al.append(temp)
    return al


def make_sec_point(lat1, lng1, lat2, lng2,):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+lat1+","+lng1+"&destination="+lat2+","+lng2+"&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    global google_request
    google_request += 1
    re = []

    if len(response.json()['routes'][0]['legs'][0]['steps']) == 1:
        #print("Google Map: ",response.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value'],", ","Calculated: ",calcCrow(float(lat1), float(lng1), float(lat2), float(lng2)))
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
    global google_request
    google_request += 1
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
    global google_request
    google_request += 1
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
    global google_request
    google_request += 1
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

def get_prev_violations_StreetID(str_id):
    ref_pointa = "0,0"

    prev_point_one = []
    prev_point_two = []

    total_violation = 0
    cnx = db_connection()
    cursor_ = cnx.cursor()
    query = (
        "SELECT `side01_ref`, `side01`, `side02`, `total_violations`, `upload_date` FROM `map_view` WHERE `streetid` ="+str(str_id)+";")
    cursor_.execute(query)
    for a, b, c, d, e in cursor_:
        ref_pointa = a
        prev_point_one = ast.literal_eval(b)
        prev_point_two = ast.literal_eval(c)
        total_violation = d

    cursor_.close()
    cnx.close()
    return ref_pointa, prev_point_one, prev_point_two, total_violation


def insert_map_view(str_id, ref, side01, side02, total):
    cnx = db_connection()
    cursor_ = cnx.cursor()
    query = (
            "INSERT INTO `map_view`(`streetid`, `side01_ref`, `side01`, `side02`, `total_violations`, `upload_date`) VALUES ("+str_id+",'"+ref+"',\""+side01+"\",\""+side02+"\","+total+",'"+datetime.today().strftime('%Y-%m-%d')+"');")
    cursor_.execute(query)

    cursor_.close()
    cnx.commit()
    cnx.close()


def insert_violations_Street(violations):
    query_data_list = []
    for j in violations:
        query_data_list.append("('" + str(j['street_id']) + "','" + str(
            j['violation_type_id']) + "','" + str(j['details']) + "','" + str(
            j['accurate']) + "','" + str(j['risk']) + "','" + str(
            j['display_img']) + "','" + str(j['lat']) + "','" + str(
            j['long']) + "','"+str(j['device_id'])+"','"+j['polygon_img']+"','" + str(
            j['violation_date']) + "','2022-10-28 " + str(
            j['violation_time']) + "','0','0','0')")

    query0 = query_data_list[0]
    for j in range(1, len(query_data_list)):
        query0 = query0 + "," + query_data_list[j]

    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
                "INSERT INTO `violation`(`street_id`, `violation_type_id`, `details`, `accurate`, `risk`, `display_img`, `lat`, `long`,`device_id`, `polygon_img`, `violation_date`, `violation_time`, `violation_status`, `action_taken`, `user_id`) VALUES " +
                query0)

    cursor.execute(query)
    cnx.commit()
    cursor.close()

    cnx.close()


def update_map_view(str_id, side01, side02, total):

    cnx = db_connection()
    cursor_ = cnx.cursor()
    query = ("UPDATE `map_view` SET `side01`=\""+side01+"\",`side02`=\""+side02+"\",`total_violations`="+total+" WHERE `streetid`="+str_id)
    cursor_.execute(query)
    cursor_.close()
    cnx.commit()
    cnx.close()


def get_distance_btw_violation_by_distance_matrix_api(lat1, lng1, lat2, lng2):
    url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat1) + "," + str(lng1) + "&destination=" + str(lat2) + "," + str(lng2) + "&mode=walking&key=" + api_text
    response1 = requests.request("GET", url1, headers={}, data={})
    global google_request
    google_request += 1
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
                list_of_street_names.append({
                    "street_id": a,
                    "street_name": b,
                    "violation": temp,
                    'side01':[],
                    'side02':[],
                    'total_violations':0,
                    'ref':"",
                    'date':''})
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
        list_of_street_names.append({"street_id": st_id, "street_name": i, "violation": temp,'side01':[],
                    'side02':[],
                    'total_violations':0,
                    'ref':"",
                    'date':''})
        #set_of_street_names.remove(i)

    #print(list_of_street_names)
    for st in list_of_street_names:
        insert_violations_Street(st['violation'])
    for street in list_of_street_names:
        ref_pointa, prev_point_one, prev_point_two, total_violation = get_prev_violations_StreetID(street['street_id'])
        if total_violation == 0:

            street['ref'] = str(street['violation'][0]['lat']) + "," + str(street['violation'][0]['long'])
            street['total_violations'] = len(street['violation'])

            if len(street['violation']) > 1:
                point_one = []
                point_two = []
                point_one.append(street['violation'][0])
                for violation in range(1, len(street['violation'])):
                    if get_distance_btw_violation_by_distance_matrix_api(street['violation'][0]['lat'],
                                                                         street['violation'][0]['long'],
                                                                         street['violation'][violation]['lat'],
                                                                         street['violation'][violation]['long']):
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
                            dist = calcCrow(point_one[violation]['lat'], point_one[violation]['long'],
                                            point_one[sec_vio]['lat'], point_one[sec_vio]['long'])
                            if max_distance < dist:
                                max_distance = dist
                                max_distance_point_01 = violation
                                max_distance_point_02 = sec_vio
                    if max_distance <= 300:
                        temp = {
                            'start_latlng': str(point_one[max_distance_point_01]['lat']) + "," + str(
                                point_one[max_distance_point_01]['long']),
                            'end_latlng': str(point_one[max_distance_point_02]['lat']) + "," + str(
                                point_one[max_distance_point_02]['long']),
                            'polylines': make_responce_of_two_point(str(point_one[max_distance_point_01]['lat']) + "," + str(
                                point_one[max_distance_point_01]['long']), str(point_one[max_distance_point_02]['lat']) + "," + str(
                                point_one[max_distance_point_02]['long']))
                        }
                        street['side01'].append(temp)

                    else:
                        sorted_points = []
                        sorted_points.append(max_distance_point_01)
                        for count in range(len(point_one) - 1):
                            min_dis = 1000000000000000
                            min_dist_point = 0
                            for violation in range(len(point_one)):
                                if violation == max_distance_point_01 or violation in sorted_points:
                                    continue
                                dist = calcCrow(point_one[violation]['lat'], point_one[violation]['long'],
                                                point_one[max_distance_point_01]['lat'],
                                                point_one[max_distance_point_01]['long'])
                                if min_dis > dist:
                                    min_dis = dist
                                    min_dist_point = violation

                            sorted_points.append(min_dist_point)
                        start_point = 0
                        last_point = -1
                        point = 0
                        while point < len(sorted_points) - 1:
                            dist = calcCrow(point_one[sorted_points[point]]['lat'],
                                            point_one[sorted_points[point]]['long'],
                                            point_one[sorted_points[point + 1]]['lat'],
                                            point_one[sorted_points[point + 1]]['long'])
                            if dist <= 300:
                                last_point = point + 1
                            else:
                                if last_point == -1:
                                    got_sec = get_second_latlng_for_single_violation_by_direction_api(
                                        point_one[sorted_points[start_point]]['lat'],
                                        point_one[sorted_points[start_point]]['long'])
                                    if len(got_sec) == 2:

                                        temp = {
                                            'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                            'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                                            'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']), str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                        }
                                        street['side01'].append(temp)

                                    else:
                                        temp = {
                                            'start_latlng': str(
                                                point_one[sorted_points[start_point]]['lat']) + "," + str(
                                                point_one[sorted_points[start_point]]['long']),
                                            'end_latlng': "0,0",
                                            'polylines': []
                                        }
                                        street['side01'].append(temp)

                                    start_point = start_point + 1
                                else:
                                    temp = {
                                        'start_latlng': str(point_one[sorted_points[start_point]]['lat']) + "," + str(
                                            point_one[sorted_points[start_point]]['long']),
                                        'end_latlng': str(point_one[sorted_points[last_point]]['lat']) + "," + str(
                                            point_one[sorted_points[last_point]]['long']),
                                        'polylines': make_responce_of_two_point( str(point_one[sorted_points[start_point]]['lat']) + "," + str(
                                            point_one[sorted_points[start_point]]['long']),
                                        str(point_one[sorted_points[last_point]]['lat']) + "," + str(
                                            point_one[sorted_points[last_point]]['long']))
                                    }
                                    street['side01'].append(temp)

                                    start_point = last_point + 1
                                    last_point = -1
                            point = point + 1

                else:
                    # point_one[0]['start_latlng'] = str(point_one[0]['lat'])+","+str(point_one[0]['long'])
                    # point_one[0]['end_latlng'] = "0"
                    got_sec = get_second_latlng_for_single_violation_by_direction_api(
                        point_one[0]['lat'], point_one[0]['long'])
                    if len(got_sec) == 2:
                        temp = {
                            'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                            'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                            'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                            str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                        }
                        street['side01'].append(temp)

                    else:
                        temp = {
                            'start_latlng': str(point_one[0]['lat']) + "," + str(point_one[0]['long']),
                            'end_latlng': "0,0"
                        }
                        street['side01'].append(temp)

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
                        temp = {
                            'start_latlng': str(
                                point_two[max_distance_point_01]['lat']) + "," + str(
                                point_two[max_distance_point_01]['long']),
                            'end_latlng': str(
                                point_two[max_distance_point_02]['lat']) + "," + str(
                                point_two[max_distance_point_02]['long']),
                            'polylines': make_responce_of_two_point(str(
                                point_two[max_distance_point_01]['lat']) + "," + str(
                                point_two[max_distance_point_01]['long']),
                            str(
                                point_two[max_distance_point_02]['lat']) + "," + str(
                                point_two[max_distance_point_02]['long']))
                        }
                        street['side02'].append(temp)

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
                            dist = calcCrow(point_two[sorted_points[point]]['lat'],
                                            point_two[sorted_points[point]]['long'],
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
                                        temp = {
                                            'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                            'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                                            'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                             str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                        }
                                        street['side02'].append(temp)


                                    else:
                                        temp = {
                                            'start_latlng': str(
                                                point_two[sorted_points[start_point]]['lat']) + "," + str(
                                                point_two[sorted_points[start_point]]['long']),
                                            'end_latlng': "0,0"
                                        }
                                        street['side02'].append(temp)

                                    start_point = start_point + 1
                                else:
                                    temp = {
                                        'start_latlng': str(
                                            point_two[sorted_points[start_point]]['lat']) + "," + str(
                                            point_two[sorted_points[start_point]]['long']),
                                        'end_latlng': str(
                                            point_two[sorted_points[last_point]]['lat']) + "," + str(
                                            point_two[sorted_points[last_point]]['long']),
                                        'polylines': make_responce_of_two_point(str(
                                            point_two[sorted_points[start_point]]['lat']) + "," + str(
                                            point_two[sorted_points[start_point]]['long']),
                                        str(
                                            point_two[sorted_points[last_point]]['lat']) + "," + str(
                                            point_two[sorted_points[last_point]]['long']))
                                    }
                                    street['side02'].append(temp)

                                    start_point = last_point + 1
                                    last_point = -1
                            point = point + 1


                elif len(point_two) == 1:

                    got_sec = get_second_latlng_for_single_violation_by_direction_api(
                        point_two[0]['lat'], point_two[0]['long'])

                    if len(got_sec) == 2:

                        temp = {
                            'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                            'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                            'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                             str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                        }
                        street['side02'].append(temp)

                    else:
                        temp = {
                            'start_latlng': str(point_two[0]['lat']) + "," + str(point_two[0]['long']),
                            'end_latlng': "0,0"
                        }
                        street['side02'].append(temp)


            else:

                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                    street['violation'][0]['lat'], street['violation'][0]['long'])

                if len(got_sec) == 2:
                    temp = {
                        'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                        'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                        'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                         str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                    }
                    street['side01'].append(temp)

                else:
                    temp = {
                        'start_latlng': str(street['violation'][0]['lat']) + "," + str(street['violation'][0]['long']),
                        'end_latlng': "0,0"
                    }
                    street['side01'].append(temp)

            insert_map_view(str(street['street_id']), street['ref'], str(street['side01']), str(street['side02']), str(street['total_violations']))


        else:
            # ref_pointa, prev_point_one, prev_point_two, total_violation
            total_violation = total_violation + len(street['violation'])
            street['ref'] = ref_pointa
            point_one = []
            point_two = []
            for violation in range(len(street['violation'])):
                if get_distance_btw_violation_by_distance_matrix_api(street['ref'].split(',')[0],
                                                                     street['ref'].split(',')[1],
                                                                     street['violation'][violation]['lat'],
                                                                     street['violation'][violation]['long']):
                    point_one.append(street['violation'][violation])
                else:
                    point_two.append(street['violation'][violation])

            not_placed_point_one = []
            not_placed_point_two = []
            for vio in point_one:
                placed = False
                for prev_vio in range(len(prev_point_one)):

                    dist_A = calcCrow(vio['lat'],vio['long'], float(prev_point_one[prev_vio]['start_latlng'].split(',')[0]),  float(prev_point_one[prev_vio]['start_latlng'].split(',')[1]))
                    if not prev_point_one[prev_vio]['end_latlng'] == "0,0":
                        dist_B = calcCrow(vio['lat'], vio['long'], float(prev_point_one[prev_vio]['end_latlng'].split(',')[0]),
                                          float(prev_point_one[prev_vio]['end_latlng'].split(',')[1]))
                        dist_AB = calcCrow(float(prev_point_one[prev_vio]['start_latlng'].split(',')[0]),  float(prev_point_one[prev_vio]['start_latlng'].split(',')[1]), float(prev_point_one[prev_vio]['end_latlng'].split(',')[0]),
                                          float(prev_point_one[prev_vio]['end_latlng'].split(',')[1]))

                        if dist_A <= 300 or dist_B <= 300:
                            placed = True
                            if dist_A >= dist_AB and dist_B <= 300:
                                prev_point_one[prev_vio]['end_latlng'] = str(vio['lat'])+","+str(vio['long'])
                                prev_point_one[prev_vio]['polylines'] = make_responce_of_two_point(prev_point_one[prev_vio]['start_latlng'], prev_point_one[prev_vio]['end_latlng'])
                            elif dist_B >= dist_AB and dist_A <= 300:
                                prev_point_one[prev_vio]['start_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                prev_point_one[prev_vio]['polylines'] = make_responce_of_two_point(
                                    prev_point_one[prev_vio]['start_latlng'], prev_point_one[prev_vio]['end_latlng'])
                    else:
                        if dist_A <=300:
                            placed = True
                            prev_point_one[prev_vio]['end_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                            prev_point_one[prev_vio]['polylines'] = make_responce_of_two_point(
                                prev_point_one[prev_vio]['start_latlng'], prev_point_one[prev_vio]['end_latlng'])
                    if placed:

                        break
                if not placed:
                    not_placed_point_one.append(vio)

            if len(not_placed_point_one) > 1:
                max_distance = 0
                max_distance_point_01 = 0
                max_distance_point_02 = 0
                for violation in range(len(not_placed_point_one)):
                    for sec_vio in range(len(not_placed_point_one)):
                        if violation == sec_vio:
                            continue
                        dist = calcCrow(not_placed_point_one[violation]['lat'], not_placed_point_one[violation]['long'],
                                        not_placed_point_one[sec_vio]['lat'],
                                        not_placed_point_one[sec_vio]['long'])
                        if max_distance < dist:
                            max_distance = dist
                            max_distance_point_01 = violation
                            max_distance_point_02 = sec_vio
                if max_distance <= 300:
                    temp = {
                        'start_latlng': str(
                            not_placed_point_one[max_distance_point_01]['lat']) + "," + str(
                            not_placed_point_one[max_distance_point_01]['long']),
                        'end_latlng': str(
                            not_placed_point_one[max_distance_point_02]['lat']) + "," + str(
                            not_placed_point_one[max_distance_point_02]['long']),
                        'polylines': make_responce_of_two_point(str(
                            not_placed_point_one[max_distance_point_01]['lat']) + "," + str(
                            not_placed_point_one[max_distance_point_01]['long']),
                        str(
                            not_placed_point_one[max_distance_point_02]['lat']) + "," + str(
                            not_placed_point_one[max_distance_point_02]['long']))
                    }
                    prev_point_one.append(temp)

                else:
                    sorted_points = []
                    sorted_points.append(max_distance_point_01)
                    for count in range(len(not_placed_point_one) - 1):
                        min_dis = 1000000000000000
                        min_dist_point = 0
                        for violation in range(len(not_placed_point_one)):
                            if violation == max_distance_point_01 or violation in sorted_points:
                                continue
                            dist = calcCrow(not_placed_point_one[violation]['lat'],
                                            not_placed_point_one[violation]['long'],
                                            not_placed_point_one[max_distance_point_01]['lat'],
                                            not_placed_point_one[max_distance_point_01]['long'])
                            if min_dis > dist:
                                min_dis = dist
                                min_dist_point = violation

                        sorted_points.append(min_dist_point)
                    start_point = 0
                    last_point = -1
                    point = 0
                    while point < len(sorted_points) - 1:
                        dist = calcCrow(not_placed_point_one[sorted_points[point]]['lat'],
                                        not_placed_point_one[sorted_points[point]]['long'],
                                        not_placed_point_one[sorted_points[point + 1]]['lat'],
                                        not_placed_point_one[sorted_points[point + 1]]['long'])
                        if dist <= 300:
                            last_point = point + 1
                        else:
                            if last_point == -1:
                                # point_two[sorted_points[start_point]]['start_latlng'] = str(
                                #     point_two[sorted_points[start_point]]['lat']) + "," + str(
                                #     point_two[sorted_points[start_point]]['long'])
                                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                                    not_placed_point_one[sorted_points[start_point]]['lat'],
                                    not_placed_point_one[sorted_points[start_point]]['long'])
                                if len(got_sec) == 2:
                                    temp = {
                                        'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                        'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                                        'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                         str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                    }
                                    prev_point_one.append(temp)


                                else:
                                    temp = {
                                        'start_latlng': str(
                                            not_placed_point_one[sorted_points[start_point]]['lat']) + "," + str(
                                            not_placed_point_one[sorted_points[start_point]]['long']),
                                        'end_latlng': "0,0"
                                    }
                                    prev_point_one.append(temp)

                                start_point = start_point + 1
                            else:
                                temp = {
                                    'start_latlng': str(
                                        not_placed_point_one[sorted_points[start_point]]['lat']) + "," + str(
                                        not_placed_point_one[sorted_points[start_point]]['long']),
                                    'end_latlng': str(
                                        not_placed_point_one[sorted_points[last_point]]['lat']) + "," + str(
                                        not_placed_point_one[sorted_points[last_point]]['long']),
                                    'polylines': make_responce_of_two_point(str(
                                        not_placed_point_one[sorted_points[start_point]]['lat']) + "," + str(
                                        not_placed_point_one[sorted_points[start_point]]['long']),
                                    str(
                                        not_placed_point_one[sorted_points[last_point]]['lat']) + "," + str(
                                        not_placed_point_one[sorted_points[last_point]]['long']))
                                }
                                prev_point_one.append(temp)

                                start_point = last_point + 1
                                last_point = -1
                        point = point + 1

            elif len(not_placed_point_one) == 1:

                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                    not_placed_point_one[0]['lat'], not_placed_point_one[0]['long'])

                if len(got_sec) == 2:

                    temp = {
                        'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                        'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                        'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                        str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                    }
                    prev_point_one.append(temp)

                else:
                    temp = {
                        'start_latlng': str(not_placed_point_one[0]['lat']) + "," + str(
                            not_placed_point_one[0]['long']),
                        'end_latlng': "0,0"
                    }
                    prev_point_one.append(temp)

            for vio in point_two:
                placed = False
                for prev_vio in range(len(prev_point_two)):

                    dist_A = calcCrow(vio['lat'], vio['long'],
                                      float(prev_point_two[prev_vio]['start_latlng'].split(',')[0]),
                                      float(prev_point_two[prev_vio]['start_latlng'].split(',')[1]))
                    if not prev_point_two[prev_vio]['end_latlng'] == "0,0":
                        dist_B = calcCrow(vio['lat'], vio['long'],
                                          float(prev_point_two[prev_vio]['end_latlng'].split(',')[0]),
                                          float(prev_point_two[prev_vio]['end_latlng'].split(',')[1]))
                        dist_AB = calcCrow(float(prev_point_two[prev_vio]['start_latlng'].split(',')[0]),
                                           float(prev_point_two[prev_vio]['start_latlng'].split(',')[1]),
                                           float(prev_point_two[prev_vio]['end_latlng'].split(',')[0]),
                                           float(prev_point_two[prev_vio]['end_latlng'].split(',')[1]))

                        if dist_A <= 300 or dist_B <= 300:
                            placed = True
                            if dist_A >= dist_AB and dist_B <= 300:
                                prev_point_two[prev_vio]['end_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                prev_point_two[prev_vio]['polylines'] = make_responce_of_two_point(
                                    prev_point_two[prev_vio]['start_latlng'], prev_point_two[prev_vio]['end_latlng'])

                            elif dist_B >= dist_AB and dist_A <= 300:
                                prev_point_two[prev_vio]['start_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                prev_point_two[prev_vio]['polylines'] = make_responce_of_two_point(
                                    prev_point_two[prev_vio]['start_latlng'], prev_point_two[prev_vio]['end_latlng'])
                    else:
                        if dist_A <=300:
                            placed = True
                            prev_point_two[prev_vio]['end_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                            prev_point_two[prev_vio]['polylines'] = make_responce_of_two_point(
                                prev_point_two[prev_vio]['start_latlng'], prev_point_two[prev_vio]['end_latlng'])
                    if placed:
                        break
                if not placed:
                    not_placed_point_two.append(vio)

            if len(not_placed_point_two) > 1:
                max_distance = 0
                max_distance_point_01 = 0
                max_distance_point_02 = 0
                for violation in range(len(not_placed_point_two)):
                    for sec_vio in range(len(not_placed_point_two)):
                        if violation == sec_vio:
                            continue
                        dist = calcCrow(not_placed_point_two[violation]['lat'], not_placed_point_two[violation]['long'],
                                        not_placed_point_two[sec_vio]['lat'],
                                        not_placed_point_two[sec_vio]['long'])
                        if max_distance < dist:
                            max_distance = dist
                            max_distance_point_01 = violation
                            max_distance_point_02 = sec_vio
                if max_distance <= 300:
                    temp = {
                        'start_latlng': str(
                            not_placed_point_two[max_distance_point_01]['lat']) + "," + str(
                            not_placed_point_two[max_distance_point_01]['long']),
                        'end_latlng': str(
                            not_placed_point_two[max_distance_point_02]['lat']) + "," + str(
                            not_placed_point_two[max_distance_point_02]['long']),
                        'polylines': make_responce_of_two_point(str(
                            not_placed_point_two[max_distance_point_01]['lat']) + "," + str(
                            not_placed_point_two[max_distance_point_01]['long']),
                         str(
                            not_placed_point_two[max_distance_point_02]['lat']) + "," + str(
                            not_placed_point_two[max_distance_point_02]['long']))
                    }
                    prev_point_two.append(temp)

                else:
                    sorted_points = []
                    sorted_points.append(max_distance_point_01)
                    for count in range(len(not_placed_point_two) - 1):
                        min_dis = 1000000000000000
                        min_dist_point = 0
                        for violation in range(len(not_placed_point_two)):
                            if violation == max_distance_point_01 or violation in sorted_points:
                                continue
                            dist = calcCrow(not_placed_point_two[violation]['lat'],
                                            not_placed_point_two[violation]['long'],
                                            not_placed_point_two[max_distance_point_01]['lat'],
                                            not_placed_point_two[max_distance_point_01]['long'])
                            if min_dis > dist:
                                min_dis = dist
                                min_dist_point = violation

                        sorted_points.append(min_dist_point)
                    start_point = 0
                    last_point = -1
                    point = 0
                    while point < len(sorted_points) - 1:
                        dist = calcCrow(not_placed_point_two[sorted_points[point]]['lat'],
                                        not_placed_point_two[sorted_points[point]]['long'],
                                        not_placed_point_two[sorted_points[point + 1]]['lat'],
                                        not_placed_point_two[sorted_points[point + 1]]['long'])
                        if dist <= 300:
                            last_point = point + 1
                        else:
                            if last_point == -1:
                                # point_two[sorted_points[start_point]]['start_latlng'] = str(
                                #     point_two[sorted_points[start_point]]['lat']) + "," + str(
                                #     point_two[sorted_points[start_point]]['long'])
                                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                                    not_placed_point_two[sorted_points[start_point]]['lat'],
                                    not_placed_point_two[sorted_points[start_point]]['long'])
                                if len(got_sec) == 2:
                                    temp = {
                                        'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                        'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                                        'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                        str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                    }
                                    prev_point_two.append(temp)


                                else:
                                    temp = {
                                        'start_latlng': str(
                                            not_placed_point_two[sorted_points[start_point]]['lat']) + "," + str(
                                            not_placed_point_two[sorted_points[start_point]]['long']),
                                        'end_latlng': "0,0"
                                    }
                                    prev_point_two.append(temp)

                                start_point = start_point + 1
                            else:
                                temp = {
                                    'start_latlng': str(
                                        not_placed_point_two[sorted_points[start_point]]['lat']) + "," + str(
                                        not_placed_point_two[sorted_points[start_point]]['long']),
                                    'end_latlng': str(
                                        not_placed_point_two[sorted_points[last_point]]['lat']) + "," + str(
                                        not_placed_point_two[sorted_points[last_point]]['long']),
                                    'polylines': make_responce_of_two_point(str(
                                        not_placed_point_two[sorted_points[start_point]]['lat']) + "," + str(
                                        not_placed_point_two[sorted_points[start_point]]['long']),
                                    str(
                                        not_placed_point_two[sorted_points[last_point]]['lat']) + "," + str(
                                        not_placed_point_two[sorted_points[last_point]]['long']))
                                }
                                prev_point_two.append(temp)

                                start_point = last_point + 1
                                last_point = -1
                        point = point + 1

            elif len(not_placed_point_two) == 1:

                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                    not_placed_point_two[0]['lat'], not_placed_point_two[0]['long'])

                if len(got_sec) == 2:

                    temp = {
                        'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                        'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']),
                        'polylines': make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                        str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                    }
                    prev_point_two.append(temp)

                else:
                    temp = {
                        'start_latlng': str(not_placed_point_two[0]['lat']) + "," + str(
                            not_placed_point_two[0]['long']),
                        'end_latlng': "0,0"
                    }
                    prev_point_two.append(temp)

            update_map_view(str(street['street_id']), str(prev_point_one), str(prev_point_two), str(total_violation))




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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",
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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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

    "device_id":0,
    "polygon_img":"",

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
    "device_id":0,
    "polygon_img":"",
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
    "device_id":0,
    "polygon_img":"",
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

    "device_id":0,
    "polygon_img":"",

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
    "device_id":0,
    "polygon_img":"",
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
    "device_id":0,
    "polygon_img":"",
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

    "device_id":0,
    "polygon_img":"",

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
        "device_id":0,
    "polygon_img":"",
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
    "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
"device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
    "device_id": 0,
    "polygon_img": "",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
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
        "device_id":0,
    "polygon_img":"",
    },
]


x = time.perf_counter()
upload_dataset(tett)

print("Total Violations: ", len(tett))
print("Time Consume in Sec: ", time.perf_counter() - x)
print("Google Requests: ", google_request)


