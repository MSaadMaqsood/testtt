from datetime import datetime
import requests
import math
import mysql.connector
import json
import ast
import polyline
import time


# def db_connection():
#     host = 'localhost'
#     user = "root"
#     password = ""
#     database = 'elm'
#     cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
#     return cnx
#


def db_connection():
    host = '67.205.163.34'
    user = "sohail"
    password = "sohail123"
    database = 'elm1'
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
    return cnx


def get_map_api_():
    map_api = ""
    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("SELECT `api` FROM `map_api` WHERE `status` = 1;")
    cursor.execute(query)
    for a in cursor:
        map_api = a
    cursor.close()
    cnx.close()
    map_api_ = str(map_api[0])
    return map_api_


api_text = get_map_api_()
server = "http://127.0.0.1:1244"
#api_text = "AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"

google_request = 0
database_request = 0


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
    print("make_responce_of_two_point")
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+latlng1+"&destination="+latlng2+"&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    global google_request
    google_request += 1
    al = []
    final_temp = []
    if len(response.json()['routes'][0]['legs'][0]['steps']) > 1:

        #print("More than one 0001")

        url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + latlng2 + "&destination=" + latlng1 + "&key=" + api_text
        response1 = requests.request("GET", url1, headers={}, data={})
        google_request += 1
        al = []
        #print("Responce of 02",len(response1.json()['routes'][0]['legs'][0]['steps']) ,response1.json()['routes'][0]['legs'][0]['steps'])
        if len(response1.json()['routes'][0]['legs'][0]['steps']) > 1:
            #print("More than one 0002")
            # start 01
            got_sec = get_second_latlng_for_single_violation_by_direction_api(
                latlng1.split(',')[0], latlng1.split(',')[1])

            if len(got_sec) == 2:

                temp = make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                                  str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                for mb in temp:
                    final_temp.append(mb)

            else:
                temp = {
                    'start_latlng': latlng1,
                    'end_latlng': "0,0"
                }
                final_temp.append(temp)
            # end
            # start 02
            got_sec = get_second_latlng_for_single_violation_by_direction_api(
                latlng2.split(',')[0], latlng2.split(',')[1])

            if len(got_sec) == 2:

                temp = make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                                  str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                for mb in temp:
                    final_temp.append(mb)

            else:
                temp = {
                    'start_latlng': latlng2,
                    'end_latlng': "0,0"
                }
                final_temp.append(temp)
            # end
        else:
            l = polyline.decode(response1.json()["routes"][0]['overview_polyline']['points'])
            for i in l:
                temp = {'lat': i[0], 'lng': i[1]}
                al.append(temp)

            final_temp = [
                {
                    'start_latlng': latlng2,
                    'end_latlng': latlng1,
                    'polylines': al
                }
            ]
    else:
        al = []
        l = polyline.decode(response.json()["routes"][0]['overview_polyline']['points'])
        for i in l:
            temp = {'lat': i[0], 'lng': i[1]}
            al.append(temp)

        final_temp = [
            {
                'start_latlng': latlng1,
                'end_latlng': latlng2,
                'polylines': al
            }
        ]
    return final_temp


def make_responce_of_two_point_only(latlng1, latlng2):

    print("make_responce_of_two_point_only")
    print(latlng1)
    print(latlng2)
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+latlng1+"&destination="+latlng2+"&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    global google_request
    google_request += 1
    al = []
    if len(response.json()['routes'][0]['legs'][0]['steps']) > 1:
        url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + latlng2 + "&destination=" + latlng1 + "&key=" + api_text
        response1 = requests.request("GET", url1, headers={}, data={})
        google_request += 1
        al = []
        if len(response1.json()['routes'][0]['legs'][0]['steps']) > 1:
            pass
        else:
            l = polyline.decode(response1.json()["routes"][0]['overview_polyline']['points'])
            for i in l:
                temp = {'lat': i[0], 'lng': i[1]}
                al.append(temp)

    else:
        al = []
        l = polyline.decode(response.json()["routes"][0]['overview_polyline']['points'])
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
    lat = float(lat)
    long = float(long)
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

    return st_id[0]


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
        "SELECT `side01_ref`, `side01`, `side02`, `total_violations`, `upload_date` FROM `map_view` WHERE `streetid` ='"+str(str_id)+"';")
    cursor_.execute(query)
    for a, b, c, d, e in cursor_:
        ref_pointa = a
        prev_point_one = ast.literal_eval(b)
        prev_point_two = ast.literal_eval(c)
        total_violation = d

    cursor_.close()
    cnx.close()
    return ref_pointa, prev_point_one, prev_point_two, total_violation


def get_used_street_ids(str_id):
    unava_id = set()
    cnx = db_connection()
    cursor_ = cnx.cursor()
    temp = str(list(str_id))
    tempx = temp.replace('[','(')
    tempx = tempx.replace(']', ')')
    query = (
        "SELECT `streetid` FROM `street` WHERE `in_use` =1 AND `streetid` in "+tempx+";")
    cursor_.execute(query)
    tempz = []
    for a in cursor_:
        tempz.append(a)
    for i in tempz:
        try:
            unava_id.add(int(i))
        except:
            unava_id.add(int(i[0]))
    cursor_.close()
    cnx.close()
    return unava_id


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
        #j['display_img'] = "1.jpg"
        tt = str(j['display_img']).replace('.', ',')
        urlToUploadImage = server+"/uploadviolationimage/"+tt
        my_img = {'image': open('to_upload_img/'+str(j['display_img']), 'rb')}
        #my_img = {'image': open('to_upload_img/1.jpg', 'rb')}
        r = requests.post(urlToUploadImage, files=my_img)
        corr = 0
        if int(j['accurate']) >= 80:
            corr = -1
        query_data_list.append("('" + str(j['street_id']) + "','" + str(
            j['violation_type_id']) + "','" + str(j['details']) + "','" + str(
            j['accurate']) + "','" + str(j['risk']) + "','" + r.json()['name'] + "','" + str(j['lat']) + "','" + str(
            j['long']) + "','"+str(j['device_id'])+"','"+j['polygon_img']+"','" + str(
            j['violation_date']) + "','2022-10-28 " + str(
            j['violation_time']) + "','0','0',"+str(corr)+")")

    query0 = query_data_list[0]
    for j in range(1, len(query_data_list)):
        query0 = query0 + "," + query_data_list[j]

    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
                "INSERT INTO `violation`(`street_id`, `violation_type_id`, `details`, `accurate`, `risk`, `display_img`, `lat`, `long`,`device_id`, `polygon_img`, `violation_date`, `violation_time`, `violation_status`, `action_taken`, `correct`) VALUES " +
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


def update_street_status(street_ids, st):
    cnx = db_connection()
    cursor_ = cnx.cursor()
    temp = str(list(street_ids))
    tempx = temp.replace('[', '(')
    tempx = tempx.replace(']', ')')

    query = (
                "UPDATE `street` SET `in_use`="+str(st)+" WHERE `streetid` in " + tempx)
    cursor_.execute(query)
    cursor_.close()
    cnx.commit()
    cnx.close()

def get_distance_btw_violation_by_distance_matrix_api(lat1, lng1, lat2, lng2):
    url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat1) + "," + str(lng1) + "&destination=" + str(lat2) + "," + str(lng2) + "&key=" + api_text
    response1 = requests.request("GET", url1, headers={}, data={})
    global google_request
    google_request += 1
    one = response1.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value']
    if len(response1.json()['routes'][0]['legs'][0]['steps']) == 1:

        return True
    else:
        url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat2) + "," + str(
            lng2) + "&destination=" + str(lat1) + "," + str(lng1) + "&key=" + api_text
        response = requests.request("GET", url, headers={}, data={})
        if len(response.json()['routes'][0]['legs'][0]['steps']) == 1:

            return True
        else:

            return False


def retry_upload_dataset(dataset):
    print(dataset)
    set_of_street_ids = set()
    set_of_street_ava_ids = set()
    set_of_street_un_ava_ids = set()
    list_of_street_names = []
    list_unava_str = []
    list_ava_str = []
    final_list_of_data = []

    list_of_street_names = dataset
    for j in list_of_street_names:
        set_of_street_ids.add(int(j['street_id']))

    set_of_street_un_ava_ids = get_used_street_ids(set_of_street_ids)
    set_of_street_ava_ids = set_of_street_ids.difference(set_of_street_un_ava_ids)
    ############################################################3333
    if len(set_of_street_ava_ids) > 0:
        update_street_status(set_of_street_ava_ids, 1)
    for zzzz in list_of_street_names:
        if int(zzzz['street_id']) in set_of_street_ava_ids:
            list_ava_str.append(zzzz)
        else:
            list_unava_str.append(zzzz)

    for street in list_ava_str:
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
                        temp = make_responce_of_two_point(str(point_one[max_distance_point_01]['lat']) + "," + str(
                                point_one[max_distance_point_01]['long']), str(point_one[max_distance_point_02]['lat']) + "," + str(
                                point_one[max_distance_point_02]['long']))
                        for mb in temp:
                            street['side01'].append(mb)

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

                                        temp = make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']), str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                        for mb in temp:
                                            street['side01'].append(mb)

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
                                    temp = make_responce_of_two_point( str(point_one[sorted_points[start_point]]['lat']) + "," + str(
                                            point_one[sorted_points[start_point]]['long']),
                                        str(point_one[sorted_points[last_point]]['lat']) + "," + str(
                                            point_one[sorted_points[last_point]]['long']))
                                    for mb in temp:
                                        street['side01'].append(mb)

                                    start_point = last_point + 1
                                    last_point = -1
                            point = point + 1

                else:
                    # point_one[0]['start_latlng'] = str(point_one[0]['lat'])+","+str(point_one[0]['long'])
                    # point_one[0]['end_latlng'] = "0"
                    got_sec = get_second_latlng_for_single_violation_by_direction_api(
                        point_one[0]['lat'], point_one[0]['long'])
                    if len(got_sec) == 2:
                        temp =  make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                            str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))

                        for mb in temp:
                            street['side01'].append(mb)

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
                        temp =  make_responce_of_two_point(str(
                                point_two[max_distance_point_01]['lat']) + "," + str(
                                point_two[max_distance_point_01]['long']),
                            str(
                                point_two[max_distance_point_02]['lat']) + "," + str(
                                point_two[max_distance_point_02]['long']))
                        for mb in temp:
                            street['side02'].append(mb)

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
                                        temp = make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                             str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                        for mb in temp:
                                            street['side02'].append(mb)


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
                                    temp =  make_responce_of_two_point(str(
                                            point_two[sorted_points[start_point]]['lat']) + "," + str(
                                            point_two[sorted_points[start_point]]['long']),
                                        str(
                                            point_two[sorted_points[last_point]]['lat']) + "," + str(
                                            point_two[sorted_points[last_point]]['long']))
                                    for mb in temp:
                                        street['side02'].append(mb)

                                    start_point = last_point + 1
                                    last_point = -1
                            point = point + 1


                elif len(point_two) == 1:

                    got_sec = get_second_latlng_for_single_violation_by_direction_api(
                        point_two[0]['lat'], point_two[0]['long'])

                    if len(got_sec) == 2:

                        temp =  make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                             str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                        for mb in temp:
                            street['side02'].append(mb)

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
                    temp = make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                         str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))

                    for mb in temp:
                        street['side01'].append(mb)

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

                            if dist_A >= dist_AB and dist_B <= 300:

                                xx = make_responce_of_two_point_only(prev_point_one[prev_vio]['start_latlng'],
                                                                prev_point_one[prev_vio]['end_latlng'])
                                if len(xx) > 0:
                                    prev_point_one[prev_vio]['end_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                    prev_point_one[prev_vio]['polylines'] = xx
                                    placed = True
                            elif dist_B >= dist_AB and dist_A <= 300:
                                xx = make_responce_of_two_point_only(
                                        prev_point_one[prev_vio]['start_latlng'], prev_point_one[prev_vio]['end_latlng'])
                                if len(xx) > 0:
                                    prev_point_one[prev_vio]['start_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                    prev_point_one[prev_vio]['polylines'] = xx
                                    placed = True
                    else:
                        if dist_A <=300:
                            xx = make_responce_of_two_point_only(
                                prev_point_one[prev_vio]['start_latlng'], prev_point_one[prev_vio]['end_latlng'])
                            if len(xx) > 0:
                                placed = True
                                prev_point_one[prev_vio]['end_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                prev_point_one[prev_vio]['polylines'] = xx
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
                    temp =  make_responce_of_two_point(str(
                            not_placed_point_one[max_distance_point_01]['lat']) + "," + str(
                            not_placed_point_one[max_distance_point_01]['long']),
                        str(
                            not_placed_point_one[max_distance_point_02]['lat']) + "," + str(
                            not_placed_point_one[max_distance_point_02]['long']))
                    for mb in temp:
                        prev_point_one.append(mb)

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
                                    temp =  make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                         str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                    for mb in temp:
                                        prev_point_one.append(mb)


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
                                temp =  make_responce_of_two_point(str(
                                        not_placed_point_one[sorted_points[start_point]]['lat']) + "," + str(
                                        not_placed_point_one[sorted_points[start_point]]['long']),
                                    str(
                                        not_placed_point_one[sorted_points[last_point]]['lat']) + "," + str(
                                        not_placed_point_one[sorted_points[last_point]]['long']))
                                for mb in temp:
                                    prev_point_one.append(mb)

                                start_point = last_point + 1
                                last_point = -1
                        point = point + 1

            elif len(not_placed_point_one) == 1:

                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                    not_placed_point_one[0]['lat'], not_placed_point_one[0]['long'])

                if len(got_sec) == 2:

                    temp =  make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                        str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                    for mb in temp:
                        prev_point_one.append(mb)

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

                            if dist_A >= dist_AB and dist_B <= 300:
                                xx = make_responce_of_two_point_only(
                                    prev_point_two[prev_vio]['start_latlng'], prev_point_two[prev_vio]['end_latlng'])
                                if len(xx) > 0:
                                    placed = True
                                    prev_point_two[prev_vio]['end_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                    prev_point_two[prev_vio]['polylines'] = xx

                            elif dist_B >= dist_AB and dist_A <= 300:
                                xx = make_responce_of_two_point_only(
                                        prev_point_two[prev_vio]['start_latlng'], prev_point_two[prev_vio]['end_latlng'])
                                if len(xx) > 0:
                                    placed = True
                                    prev_point_two[prev_vio]['start_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                    prev_point_two[prev_vio]['polylines'] = xx
                    else:
                        if dist_A <=300:
                            xx = make_responce_of_two_point_only(
                                prev_point_two[prev_vio]['start_latlng'], prev_point_two[prev_vio]['end_latlng'])
                            if len(xx) > 0:
                                placed = True
                                prev_point_two[prev_vio]['end_latlng'] = str(vio['lat']) + "," + str(vio['long'])
                                prev_point_two[prev_vio]['polylines'] = xx
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
                    temp =  make_responce_of_two_point(str(
                            not_placed_point_two[max_distance_point_01]['lat']) + "," + str(
                            not_placed_point_two[max_distance_point_01]['long']),
                         str(
                            not_placed_point_two[max_distance_point_02]['lat']) + "," + str(
                            not_placed_point_two[max_distance_point_02]['long']))
                    for mb in temp:
                        prev_point_two.append(mb)

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
                                    temp =  make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                                        str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                                    for mb in temp:
                                        prev_point_two.append(mb)

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
                                temp =  make_responce_of_two_point(str(
                                        not_placed_point_two[sorted_points[start_point]]['lat']) + "," + str(
                                        not_placed_point_two[sorted_points[start_point]]['long']),
                                    str(
                                        not_placed_point_two[sorted_points[last_point]]['lat']) + "," + str(
                                        not_placed_point_two[sorted_points[last_point]]['long']))
                                for mb in temp:
                                    prev_point_two.append(mb)

                                start_point = last_point + 1
                                last_point = -1
                        point = point + 1

            elif len(not_placed_point_two) == 1:

                got_sec = get_second_latlng_for_single_violation_by_direction_api(
                    not_placed_point_two[0]['lat'], not_placed_point_two[0]['long'])

                if len(got_sec) == 2:

                    temp =  make_responce_of_two_point(str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
                        str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng']))
                    for mb in temp:
                        prev_point_two.append(mb)

                else:
                    temp = {
                        'start_latlng': str(not_placed_point_two[0]['lat']) + "," + str(
                            not_placed_point_two[0]['long']),
                        'end_latlng': "0,0"
                    }
                    prev_point_two.append(temp)

            update_map_view(str(street['street_id']), str(prev_point_one), str(prev_point_two), str(total_violation))
            if len(set_of_street_ava_ids) > 0:
                update_street_status(set_of_street_ava_ids, 0)

    return list_unava_str


def get_google_count():
    return google_request


def set_google_count():
    global google_request
    google_request = 0


tett = [


]
