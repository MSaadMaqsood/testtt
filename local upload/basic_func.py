import json
import mysql.connector
import math
import requests
import ast

server = "http://67.205.163.34:1244"
#server = "http://127.0.0.1:1244"

# def db_connection():
#     host = 'localhost'
#     user = "root"
#     password = ""
#     database = 'elm'
#     cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
#     return cnx

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


def get_prev_violation_last_3_day(udate):
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


def calcCrow(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = (lat2-lat1) * math.pi / 180
    dLon = (lon2-lon1)* math.pi / 180
    lat1 = (lat1)* math.pi / 180
    lat2 = (lat2)* math.pi / 180

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d*1000


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


def get_list_of_streets():
    streets_list = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
        "SELECT `streetid`, `streetname` FROM `street` ORDER BY `streetid` ASC;")
    cursor.execute(query)
    for a, b in cursor:
        streets_list.append({
            'id': a,
            'name': b
        })
    return streets_list


def get_used_street_ids(str_id):

    unava_id = set()
    if len(str_id)>0:
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


def upload_new_street_name(name):
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
        "INSERT INTO `street`(`streetname`, `in_use`) VALUES ('"+name+"',0);")
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


def get_street_name(lat, long):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat)+","+str(long) + "&destination=" + str(lat)+","+str(long+0.000005) +  "&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    try:
        temp1 = response.json()['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split("on")
    except:
        return "Unknown road"

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
            return "Unknown road"


def get_prev_violations_StreetID(str_id, upload_date):
    ref_pointa = {'min': 0, 'max': 0}
    ref_pointb = {'min': 0, 'max': 0}
    prev_point_one = []
    prev_point_two = []


    total_violation = 0
    cnx = db_connection()
    cursor_ = cnx.cursor()

    query = (
        "SELECT `side01_ref`,`side02_ref`, `side01`, `side02`, `total_violations` FROM `map_view` WHERE `streetid` ='"+str(str_id)+"' and `upload_date` ='"+upload_date+"';")
    cursor_.execute(query)

    for a, b, c, d, e in cursor_:
        ref_pointa = ast.literal_eval(a)
        ref_pointb = ast.literal_eval(b)
        prev_point_one = ast.literal_eval(c)
        prev_point_two = ast.literal_eval(d)
        total_violation = e

    cursor_.close()
    cnx.close()

    return ref_pointa, ref_pointb, prev_point_one, prev_point_two, total_violation


def get_prev_violations_tree_StreetID(str_id, upload_date):
    ref_pointa = "0,0"
    ref_pointb = "0,0"
    prev_point_one = []
    prev_point_two = []


    total_violation = 0
    cnx = db_connection()
    cursor_ = cnx.cursor()

    query = (
        "SELECT `side01_ref`,`side02_ref`, `side01`, `side02`, `total_violations` FROM `map_tree_view` WHERE `streetid` ='"+str(str_id)+"' and `upload_date` ='"+upload_date+"';")
    cursor_.execute(query)

    for a, b, c, d, e in cursor_:
        ref_pointa = ast.literal_eval(a)
        ref_pointb = ast.literal_eval(b)
        prev_point_one = ast.literal_eval(c)
        prev_point_two = ast.literal_eval(d)
        total_violation = e

    cursor_.close()
    cnx.close()

    return ref_pointa, ref_pointb, prev_point_one, prev_point_two, total_violation


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


def insert_map_view(str_id, upload_date, ref01, ref02, side01, side02, total):
    cnx = db_connection()
    cursor_ = cnx.cursor()

    ref01 = str(ref01).replace("\"", "'")
    ref02 = str(ref02).replace("\"", "'")

    side01 = str(side01).replace("\"", "'")
    side02 = str(side02).replace("\"", "'")

    query = (
            "INSERT INTO `map_view`(`streetid`, `side01_ref`, `side02_ref`, `side01`, `side02`, `total_violations`, `upload_date`) VALUES ("+str(str_id)+",\""+str(ref01)+"\",\""+str(ref02)+"\",\""+str(side01)+"\",\""+str(side02)+"\","+str(total)+",'"+upload_date+"');")
    cursor_.execute(query)

    cursor_.close()
    cnx.commit()
    cnx.close()


def update_map_view(str_id, side01, side02, total, udate):
    cnx = db_connection()
    cursor_ = cnx.cursor()
    side01 = str(side01).replace("\"", "'")
    side02 = str(side02).replace("\"", "'")
    query = ("UPDATE `map_view` SET `side01`=\""+side01+"\",`side02`=\""+side02+"\",`total_violations`="+total+" WHERE `streetid`="+str(str_id)+" and `upload_date`='"+udate+"'")
    cursor_.execute(query)
    cursor_.close()
    cnx.commit()
    cnx.close()


def insert_map_view_tree(str_id, upload_date, ref01, ref02, side01, side02, total):
    cnx = db_connection()
    cursor_ = cnx.cursor()
    ref01 = str(ref01).replace("\"", "'")
    ref02 = str(ref02).replace("\"", "'")
    side01 = str(side01).replace("\"", "'")
    side02 = str(side02).replace("\"", "'")

    query = (
            "INSERT INTO `map_tree_view`(`streetid`, `side01_ref`, `side02_ref`, `side01`, `side02`, `total_violations`, `upload_date`) VALUES ("+str(str_id)+",\""+str(ref01)+"\",\""+str(ref02)+"\",\""+str(side01)+"\",\""+str(side02)+"\","+str(total)+",'"+upload_date+"');")
    cursor_.execute(query)

    cursor_.close()
    cnx.commit()
    cnx.close()


def update_map_view_tree(str_id, side01, side02, total,udate):
    cnx = db_connection()
    cursor_ = cnx.cursor()
    side01 = str(side01).replace("\"", "'")
    side02 = str(side02).replace("\"", "'")
    query = ("UPDATE `map_tree_view` SET `side01`=\""+side01+"\",`side02`=\""+side02+"\",`total_violations`="+total+" WHERE `streetid`="+str(str_id)+" and `upload_date`='"+udate+"'")
    cursor_.execute(query)
    cursor_.close()
    cnx.commit()
    cnx.close()


def insert_violations_Street(violations):
    query_data_list = []

    for j in violations:
        tt = str(j['display_img']).replace('.', ',')
        urlToUploadImage = server+"/uploadviolationimage/"+tt
        jjjj = {'image': j['string_img']}
        r = requests.post(urlToUploadImage, json=jjjj)

        query_data_list.append("('" + str(j['street_id']) + "','" + str(
            j['violation_type_id']) + "','" + str(j['details']) + "','" + str(
            j['accurate']) + "','" + str(j['risk']) + "','" + r.json()['name'] + "','" + str(j['lat']) + "','" + str(
            j['lng']) + "','"+str(j['device_id'])+"','"+j['polygon_img']+"','" + str(
            j['violation_date']) + "','2022-10-28 " + str(
            j['violation_time']) + "','0','0',"+str(j['correct'])+",'"+str(j['super_violation_id'])+"',-1)")

    query0 = query_data_list[0]
    for j in range(1, len(query_data_list)):
        query0 = query0 + "," + query_data_list[j]

    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
                "INSERT INTO `violation`(`street_id`, `violation_type_id`, `details`, `accurate`, `risk`, `display_img`, `lat`, `long`,`device_id`, `polygon_img`, `violation_date`, `violation_time`, `violation_status`, `action_taken`, `correct`, `super_violation_id`,`sensitivity`) VALUES " +
                query0)

    cursor.execute(query)
    cnx.commit()
    cursor.close()

    cnx.close()
