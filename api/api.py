import numpy as np
from flask import Flask, jsonify
from requests import request
import mysql.connector
from flask import request
from flask_cors import CORS
from flask import send_file
from datetime import datetime, timedelta
from pdfmaker02 import *
from collections import Counter
from upload_api_03 import *
import cv2
import base64
from db import *


app = Flask(__name__)
CORS(app)


def convertDateTimetoImageName(datetime):
    datetime=datetime.replace("-","")
    datetime=datetime.replace(":","")
    datetime=datetime.replace(".","")
    datetime=datetime.replace(" ","")
    return datetime





# def db_connection():
#     host = '67.205.163.34'
#     user = "sohail"
#     password = "sohail123"
#     database = 'elm1'
#     cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
#     return cnx
#


@app.route('/get_map_api_')
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
    return {'api': map_api}


@app.route('/show_violation_image/<image_name>')
def show_violation_image(image_name):
    filename = image_name
    filepath = "./images/"+filename
    return send_file(filepath, mimetype='image/gif')


@app.route('/uploadviolationimage/<iname>', methods = ['POST'])
def uploadviolationimage(iname):
    #####
    req = request.json
    img_str = req['image']
    iname = iname.replace(',', '.')

    newnameforimage = str(datetime.now())
    newnameforimage = convertDateTimetoImageName(newnameforimage) + iname
    # decode the image
    jpg_original = base64.b64decode(img_str)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imwrite("./images/"+newnameforimage, img)
    ###
    # image = request.files['image']
    # image.save("./images/"+newnameforimage)

    return jsonify({'name': newnameforimage})


@app.route('/uploadtreeimage/<iname>', methods = ['POST'])
def uploadtreeimage(iname):
    #####
    req = request.json
    img_str = req['image']
    iname = iname.replace(',', '.')

    newnameforimage = str(datetime.now())
    newnameforimage = convertDateTimetoImageName(newnameforimage) + iname
    # decode the image
    jpg_original = base64.b64decode(img_str)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imwrite("./tree_images/"+newnameforimage, img)
    ###
    # image = request.files['image']
    # image.save("./images/"+newnameforimage)

    return jsonify({'name': newnameforimage})


@app.route('/getpdf/<pdf_name>')
def getpdf(pdf_name):
    filename = pdf_name
    filepath = "./pdf/"+filename
    return send_file(filepath)


@app.route('/insertviolationdata', methods = ['POST'])
def inserttelemetryData():
    request_data=request.get_json()
    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("INSERT INTO `violation`(`street_id`, `violation_type_id`, `details`, `accurate`, `risk`, `display_img`, `lat`, `long`, `start_latlng`, `end_latlng`, `violation_date`, `violation_time`, `violation_status`, `action_taken`, `user_id`) VALUES " + request_data['query'])
    cursor.execute(query)
    cnx.commit()
    cursor.close()

    cnx.close()

    return jsonify(True)

"""################################### Dashboard ######################################################"""


@app.route('/get_dashboard')
def get_dashboard():

    data_map = violation_map_data()
    tree_data = violation_tree_map_data()
    return jsonify({"street_health": 95, "green_index": 95, "risk": 5, "data_map": data_map,"tree_data":tree_data})



def violation_map_data():
    now = datetime.today()
    today_date = now.strftime("%Y-%m-%d")
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
                "SELECT `streetid`, `side01`, `side02` FROM `map_view` WHERE 1;")
    cursor.execute(query)
    used = []
    list_for_circle = []
    for a, b, c in cursor:

        for i in ast.literal_eval(b):
            if i['ending'] == '0,0':
                temp_start = i['starting'].split(',')
                list_for_circle.append({"street_id": a,
                                        "lat": float(temp_start[0]),
                                        "lng": float(temp_start[1]), })
            else:
                used.append({"street_id": a, 'poly': i['polylines']})

        for i in ast.literal_eval(c):
            if i['ending'] == '0,0':
                temp_start = i['starting'].split(',')
                list_for_circle.append({"street_id": a,
                                        "lat": float(temp_start[0]),
                                        "lng": float(temp_start[1]), })
            else:
                used.append({"street_id": a, 'poly': i['polylines']})



    return {'line': used, 'circle': list_for_circle}

def violation_tree_map_data():
    now = datetime.today()
    today_date = now.strftime("%Y-%m-%d")
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
                "SELECT `streetid`, `side01`, `side02` FROM `map_tree_view` WHERE 1;")
    cursor.execute(query)
    used = []
    list_for_circle = []
    for a, b, c in cursor:

        for i in ast.literal_eval(b):
            if i['ending'] == '0,0':
                temp_start = i['starting'].split(',')
                list_for_circle.append({"street_id": a,
                                        "lat": float(temp_start[0]),
                                        "lng": float(temp_start[1]), })
            else:
                used.append({"street_id": a, 'poly': i['polylines']})

        for i in ast.literal_eval(c):
            if i['ending'] == '0,0':
                temp_start = i['starting'].split(',')
                list_for_circle.append({"street_id": a,
                                        "lat": float(temp_start[0]),
                                        "lng": float(temp_start[1]), })
            else:
                used.append({"street_id": a, 'poly': i['polylines']})



    return {'line': used, 'circle': list_for_circle}

"""################################### Violation Page ######################################################"""


def get_street_list_by_id(street_id):
    street_name = ""
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
        "SELECT `streetid`, `streetname` FROM `street` ORDER BY `streetid` ASC;")
    cursor.execute(query)

    for a, b in cursor:
        if int(street_id) == a:
            street_name = b
        else:
            data.append({"street_id": a, "street_name": b})
    cursor.close()
    cnx.close()
    return data, street_name


@app.route('/get_violation_page/<street_id>')
def get_violation_page(street_id):
    street_ls, street_nm = get_street_list_by_id(street_id)
    violation_table, violation_count = get_violation_table_now_default(street_id)
    return jsonify({
        "street_name": street_nm,
        "street_health": get_street_health(street_id, violation_count),
        "violation_table": violation_table,
        "list_of_streets": street_ls
    })


def get_street_health(street_id, violation_count):
    Asphalt = Sidewalk = Lighting = Cleanliness = Afforestation = Fossils = 100
    Rubble_source = Street_Sweeping = Median = Communication_tower = Fly_Poster = 100

    Total_Min_Asphalt = Total_Maj_Asphalt = Total_Sidewalk = Total_Lighting = Total_Cleanliness = 0
    Total_Afforestation = Total_Fossils = Total_Rubble_source = Total_Street_Sweeping = 0
    Total_Median = Total_Communication_tower = Total_Fly_Poster =0

    violation_count.sort()
    c = Counter(violation_count)
    a = list(c.keys())
    b = list(c.values())

    for i in range(len(a)):
        if int(a[i]) == 1:
            Asphalt = Asphalt - b[i] * 3
            Total_Min_Asphalt = b[i]
            if Asphalt < 0:
                Asphalt = 0
            continue
        elif int(a[i]) == 2:
            Sidewalk = 100 - b[i] * 2
            Total_Sidewalk = b[i]
            print(Sidewalk, b[i])
            if Sidewalk < 0:
                Sidewalk = 0
            continue
        elif int(a[i]) == 3:
            Lighting = 100 - b[i] * 2
            Total_Lighting  = b[i]
            if Lighting < 0:
                Lighting = 0
            continue
        elif int(a[i]) == 4:
            Cleanliness = 100 - b[i] * 2
            Total_Cleanliness = b[i]
            if Cleanliness < 0:
                Cleanliness = 0
            continue
        elif int(a[i]) == 5:
            Afforestation = 100 - b[i] * 2
            Total_Afforestation = b[i]
            if Afforestation < 0:
                Afforestation = 0
            continue
        elif int(a[i]) == 6:
            Fossils = 100 - b[i] * 2
            Total_Fossils = b[i]
            if Fossils < 0:
                Fossils = 0
            continue
        elif int(a[i]) == 7:
            Asphalt = Asphalt - b[i] * 6
            Total_Maj_Asphalt = b[i]
            if Asphalt < 0:
                Asphalt = 0
            continue
        elif int(a[i]) == 8:
            Rubble_source = Rubble_source - b[i] * 2
            Total_Rubble_source = b[i]
            if Rubble_source < 0:
                Rubble_source = 0
            continue
        elif int(a[i]) == 9:
            Street_Sweeping = Street_Sweeping - b[i] * 2
            Total_Street_Sweeping = b[i]
            if Street_Sweeping < 0:
                Street_Sweeping = 0
            continue
        elif int(a[i]) == 10:
            Median = Median - b[i] * 2
            Total_Median = b[i]
            if Median < 0:
                Median = 0
            continue
        elif int(a[i]) == 11:
            Communication_tower = Communication_tower - b[i] * 2
            Total_Communication_tower = b[i]
            if Communication_tower < 0:
                Communication_tower = 0
            continue
        elif int(a[i]) == 12:
            Fly_Poster = Fly_Poster - b[i] * 2
            Total_Fly_Poster = b[i]
            if Fly_Poster < 0:
                Fly_Poster = 0
            continue

    green_index = int((Asphalt+Sidewalk+Lighting+Cleanliness+Afforestation+Fossils+Rubble_source+Street_Sweeping+Median+Communication_tower+Fly_Poster)/11)
    return {
                "street_risk_rate": 100-green_index,
                "green_index": green_index,
                "Asphalt": Asphalt,
                "Sidewalk": Sidewalk,
                "Lighting": Lighting,
                "Cleanliness": Cleanliness,
                "Afforestation": Afforestation,
                "Fossils": Fossils,
                "Rubble_source": Rubble_source,
                "Street_Sweeping": Street_Sweeping,
                "Median": Median,
                "Communication_tower": Communication_tower,
                "Fly_Poster": Fly_Poster,

                "Total_Min_Asphalt": Total_Min_Asphalt,
                "Total_Maj_Asphalt": Total_Maj_Asphalt,
                "Total_Sidewalk": Total_Sidewalk,
                "Total_Lighting": Total_Lighting,
                "Total_Cleanliness": Total_Cleanliness,
                "Total_Afforestation": Total_Afforestation,
                "Total_Fossils": Total_Fossils,
                "Total_Rubble_source": Total_Rubble_source,
                "Total_Street_Sweeping": Total_Street_Sweeping,
                "Total_Median": Total_Median,
                "Total_Communication_tower": Total_Communication_tower,
                "Total_Fly_Poster": Total_Fly_Poster
            }



def get_street_list():
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
        "SELECT `streetid`, `streetname` FROM `street` ORDER BY `streetid` ASC;")
    cursor.execute(query)

    for a, b in cursor:
        data.append({"street_id": a, "street_name": b})
    cursor.close()
    cnx.close()
    return data

def get_tree_count(street_id, st_date= ""):
    street_count = 0
    cnx = db_connection()
    cursor = cnx.cursor()
    if st_date == "":
        query = (
            "SELECT `streetid`, `total_violations` FROM `map_tree_view` WHERE `streetid` = "+str(street_id)+" ORDER BY `upload_date` DESC;")
    else:
        query = (
                "SELECT `streetid`, `total_violations` FROM `map_tree_view` WHERE `streetid` = " + str(
            street_id) + " and `upload_date` = '"+str(st_date)+"';")
    cursor.execute(query)

    for a, b in cursor:
        street_count = int(b)
    cursor.close()
    cnx.close()
    return street_count


def get_violation_table_now_default(street_id):
    violation_count_list = []
    now = datetime.today()
    today_date = now.strftime("%Y-%m-%d")
    yesterday_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    violation_table_data = list()
    pages = 0
    cnx = db_connection()
    cursor = cnx.cursor()
    # query = (
    #             "SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.street_id=" + str(
    #         street_id) + " AND (violation.violation_date='"+today_date+"' OR violation.violation_date='"+yesterday_date+"' );")
    query = ("SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.correct != -2 and violation.correct != 2 and violation.street_id=" + str(
        street_id) + ";")

    cursor.execute(query)

    for a, b, c, d, e, f, g, h in cursor:
        violation_table_data.append({
            "violation_id": a,
            "violation_type_id": b,
            "accurate": c,
            "risk": d,
            "display_img": e,
            "violation_date": f.strftime('%b %d, %Y'),
            "violation_time": g.strftime('%H:%M'),
            "violation_name": h
        })
        violation_count_list.append(b)
    pages = math.floor(len(violation_table_data) / 5)
    if not (len(violation_table_data) % 5 == 0):
        pages = pages + 1
    cursor.close()
    cnx.close()
    return {"myData": violation_table_data, "pages": pages, "tree_Count": get_tree_count(street_id)}, violation_count_list


@app.route('/get_violation_table_by_date/<street_id>/<fdate>')
def get_violation_table_by_date(street_id, fdate):
    fdate_list = fdate.split(',')
    day = fdate_list[2]
    mon = fdate_list[1]
    year = fdate_list[0]
    new_date = year+'-'+mon+'-'+day

    violation_table_data = list()
    pages = 0
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
            "SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.correct != -2 and violation.correct != 2 and violation.street_id=" + str(
        street_id) + " AND violation.violation_date='"+new_date+"';")
    cursor.execute(query)

    for a, b, c, d, e, f, g, h in cursor:
        violation_table_data.append({
            "violation_id": a,
            "violation_type_id": b,
            "accurate": c,
            "risk": d,
            "display_img": e,
            "violation_date": f.strftime('%b %d, %Y'),
            "violation_time": g.strftime('%H:%M'),
            "violation_name": h
        })
    pages = math.floor(len(violation_table_data) / 5)
    if not (len(violation_table_data) % 5 == 0):
        pages = pages + 1
    cursor.close()
    cnx.close()
    return {"myData": violation_table_data, "pages": pages, "tree_Count": get_tree_count(street_id, new_date)}


@app.route('/get_single_violation/<violation_id>')
def get_single_violation(violation_id):

    violation_table_data = {
            "violation_id": 0,
            "violation_type_id": 0,
            "accurate": 0,
            "risk": 0,
            "display_img": "0",
            "violation_date": "JAn 00, 0000",
            "violation_time": "00:00",
            "violation_name": "",
            "lat": 0,
            "lng": 0,
            "status": "Not Reported",

        }
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
            "SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname, violation.lat, violation.long, violation.violation_status FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.violation_id="+violation_id+";")
    cursor.execute(query)
    for a, b, c, d, e, f, g, h, i, j, k in cursor:
        st = "Not Reported"
        if k != "0":
            st = "Reported"
        violation_table_data={
            "violation_id": a,
            "violation_type_id": b,
            "accurate": c,
            "risk": d,
            "display_img": e,
            "violation_date": f.strftime('%b %d, %Y'),
            "violation_time": g.strftime('%H:%M'),
            "violation_name": h,
            "lat": float(i),
            "lng": float(j),
            "status": st,

        }
    cursor.close()
    cnx.close()
    return violation_table_data


@app.route('/export_violation_pdf', methods = ['POST'])
def export_dashboard_csv():

    x = request.get_json()
    print(x['violation_table_data'])
    pdf_name = pdf_maker(x['street_name'], x['street_info'], x['violation_date'], x['violation_table_data']['myData'])
    return {"pdf_name": pdf_name}

# Map API
@app.route('/insertmapapi', methods = ['POST'])
def insertmapapi():
    request_data = request.get_json()
    now = datetime.today()
    today_date = now.strftime("%Y-%m-%d")
    cnx = db_connection()

    cursor1 = cnx.cursor()
    query1 = ("UPDATE `map_api` SET `status`=0")
    cursor1.execute(query1)
    cnx.commit()
    cursor1.close()

    cursor = cnx.cursor()
    query = ("INSERT INTO `map_api`(`api`, `comment`, `userid`, `entry_date`, `status`) VALUES ('"+str(request_data['api'])+"','"+str(request_data['comment'])+"','"+str(request_data['userid'])+"','"+today_date+"',1)")
    cursor.execute(query)
    cnx.commit()
    cursor.close()

    cnx.close()

    return jsonify(True)


@app.route('/get_map_api')
def get_map_api():
    map_api = {"api": "", "comment": ""}
    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("SELECT `api`, `comment`  FROM `map_api` WHERE `status` = 1;")
    cursor.execute(query)
    for a, b in cursor:
        map_api['api'] = a
        map_api['comment'] = b
    cursor.close()
    cnx.close()
    return map_api


# SELECT `street`.`streetid`,`street`.`streetname`, COUNT(1) FROM `street` INNER JOIN `violation` ON `violation`.`street_id` = `street`.`streetid` WHERE `violation`.`correct` = 0 GROUP BY `street`.`streetid`;



@app.route('/get_userlog_list_all')
def get_userlog_list_all():

    users = []
    cnx = db_connection()

    # ###################
    cursor01 = cnx.cursor()
    query01 = (
        "SELECT `user_id`, `fullname`, `position` FROM `users`;")
    cursor01.execute(query01)
    for a, b, c in cursor01:
        users.append({
            "user_id": a,
            "fullname": b,
            "position": c
        })
    cursor01.close()
    cnx.close()

    return {"users": users}



def get_vio_for_verify():
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("SELECT `violationtypeid`, `violationname` FROM `violation_type`;")
    cursor.execute(query)
    for a, b in cursor:
        data.append({
            "vio_id":a,
            "name": b,
        })
    cursor.close()
    cnx.close()
    return data


@app.route('/get_street_vio_Verify/<street_id>')
def get_street_vio_Verify(street_id):
    violation_count_list = []
    now = datetime.today()
    today_date = now.strftime("%Y-%m-%d")
    yesterday_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    violation_table_data = list()
    pages = 0
    cnx = db_connection()
    cursor = cnx.cursor()
    # query = (
    #             "SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.street_id=" + str(
    #         street_id) + " AND (violation.violation_date='"+today_date+"' OR violation.violation_date='"+yesterday_date+"' );")
    query = ("SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.street_id=" + str(
        street_id) + " AND violation.correct = -1;")

    cursor.execute(query)

    for a, b, c, d, e, f, g, h in cursor:
        violation_table_data.append({
            "violation_id": a,
            "violation_type_id": b,
            "accurate": c,
            "risk": d,
            "display_img": e,
            "violation_date": f.strftime('%b %d, %Y'),
            "violation_time": g.strftime('%H:%M'),
            "violation_name": h
        })
        violation_count_list.append(b)
    pages = math.floor(len(violation_table_data) / 5)
    if not (len(violation_table_data) % 5 == 0):
        pages = pages + 1
    cursor.close()
    cnx.close()
    vio = get_vio_for_verify()
    print(vio)
    return {"myData": violation_table_data, "pages": pages, "vio": vio}


@app.route('/update_violation_for_verify', methods = ['POST'])
def update_violation_for_verify():
    # user_id, violation_id, updated_vio_id, updated_street_id, cor, sensitivity

    request_data = request.get_json()

    prev_violation_type_id = 0
    prev_street_id = 0

    updated_violation_type_id = int(request_data['updated_vio_id'])
    updated_street_id = int(request_data['updated_street_id'])

    user_id = int(request_data['user_id'])
    violation_id = int(request_data['violation_id'])

    correct = int(request_data['cor'])
    sensitivity = int(request_data['sensitivity'])

    now = datetime.today()
    today_date = now.strftime("%Y-%m-%d")
    try:
        cnx = db_connection()

        cursor_select = cnx.cursor()
        query2 = ("SELECT `street_id`,`violation_type_id`, `lat`, `long`, `violation_date` FROM `violation` WHERE `violation_id`="+str(violation_id)+";")
        cursor_select.execute(query2)
        x = []
        udate = ""

        for a, b, c, d, e in cursor_select:
            prev_street_id = a
            prev_violation_type_id = b
            st_id = a
            if updated_street_id != 0:
                st_id = updated_street_id
            else:
                updated_street_id = a
            if updated_violation_type_id == 0:
                updated_violation_type_id = b
            x = [{
                    "street_id": st_id,
                    "violation_type_id":b,
                    "lat": float(c),
                    "long": float(d),
            }]
            udate = e.strftime('%Y-%m-%d')

        if correct == 1 and sensitivity == 1:
            x = main_function(x, udate)
            while len(x) > 0:
                time.sleep(60)
                x = main_function(x)

        cursor1 = cnx.cursor()
        query1 = ("UPDATE `violation` SET `correct`='"+str(correct)+"', `violation_type_id`='"+str(updated_violation_type_id)+"', `street_id`='"+str(updated_street_id)+"', sensitivity='"+str(sensitivity)+"' WHERE `violation_id`="+str(violation_id)+";")
        cursor1.execute(query1)
        cnx.commit()
        cursor1.close()

        cursor = cnx.cursor()
        if updated_violation_type_id != prev_violation_type_id and updated_street_id != prev_street_id:
            query = ("INSERT INTO `user_log`( `user_id`, `violation_id`, `prev_violation`, `updated_violation`, `prev_street`, `updated_street`, `correct_incorrect`,`sensitivity`, `duplicate_main_id`, `duplicated`, `entry_date`) VALUES ('"+str(user_id)+"','"+str(violation_id)+"','"+str(prev_violation_type_id)+"','"+str(updated_violation_type_id)+"','"+str(prev_street_id)+"','"+str(updated_street_id)+"','"+str(correct)+"','"+str(sensitivity)+"',0,0,'"+today_date+"')")
        elif updated_violation_type_id != prev_violation_type_id and updated_street_id == prev_street_id:
            query = (
                        "INSERT INTO `user_log`( `user_id`, `violation_id`, `prev_violation`, `updated_violation`, `prev_street`, `updated_street`, `correct_incorrect`,`sensitivity`, `duplicate_main_id`, `duplicated`, `entry_date`) VALUES ('" + str(
                    user_id) + "','" + str(violation_id) + "','" + str(prev_violation_type_id) + "','" + str(
                    updated_violation_type_id) + "','" + str(prev_street_id) + "','" + str(0) + "','" + str(
                    correct) + "','"+str(sensitivity)+"',0,0,'" + today_date + "')")
        elif updated_violation_type_id == prev_violation_type_id and updated_street_id != prev_street_id:
            query = (
                        "INSERT INTO `user_log`( `user_id`, `violation_id`, `prev_violation`, `updated_violation`, `prev_street`, `updated_street`, `correct_incorrect`,`sensitivity`, `duplicate_main_id`, `duplicated`, `entry_date`) VALUES ('" + str(
                    user_id) + "','" + str(violation_id) + "','" + str(prev_violation_type_id) + "','" + str(
                    0) + "','" + str(prev_street_id) + "','" + str(updated_street_id) + "','" + str(
                    correct) + "','"+str(sensitivity)+"',0,0,'" + today_date + "')")
        else:
            query = (
                    "INSERT INTO `user_log`( `user_id`, `violation_id`, `prev_violation`, `updated_violation`, `prev_street`, `updated_street`, `correct_incorrect`,`sensitivity`, `duplicate_main_id`, `duplicated`, `entry_date`) VALUES ('" + str(
                user_id) + "','" + str(violation_id) + "','" + str(prev_violation_type_id) + "','" + str(
                0) + "','" + str(prev_street_id) + "','" + str(0) + "','" + str(
                correct) + "','"+str(sensitivity)+"',0,0,'" + today_date + "')")
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        cnx.close()

        return {'result': 1}
    except Exception as e:
        print(e)
        return {'result': 0}


@app.route('/get_single_violation_Verify/<violation_id>')
def get_single_violation_Verify(violation_id):

    violation_table_data = {
            "violation_id": 0,
            "violation_type_id": 0,
            "violation_name": "",
            "street_id": 0,
            "street_name": "",
            "accurate": 0,
            "risk": 0,
            "display_img": "",
            "violation_date": "",
            "violation_time": "",
            "lat": 0,
            "lng": 0,
            "correct": -1,
            "current_status": "Not Reported",
            "new_violation_type_id": 0,
            "new_street_id": 0,
            "sensitivity": -1
        }
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
            "SELECT violation.violation_id, violation.violation_type_id, violation_type.violationname, violation.street_id, street.streetname, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation.lat, violation.long, violation.correct, violation.action_taken FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id INNER JOIN street ON street.streetid = violation.street_id WHERE violation.violation_id="+str(violation_id)+";")
    cursor.execute(query)
    for a, b, c, d, e, f, g, h, i, j, k, l, m, n in cursor:
        cs = "Not Reported"
        if n == 1:
            cs = "Reported"

        violation_table_data={
            "violation_id": a,
            "violation_type_id": b,
            "violation_name": c,
            "street_id": d,
            "street_name": e,
            "accurate": f,
            "risk": g,
            "display_img": h,
            "violation_date": i.strftime('%b %d, %Y'),
            "violation_time": j.strftime('%H:%M'),
            "lat": float(k),
            "lng": float(l),
            "correct": m,
            "current_status": cs,

            "new_violation_type_id": 0,
            "new_street_id": 0,
            "sensitivity": -1
        }
        print(m)
    cursor.close()
    cnx.close()
    return violation_table_data


@app.route('/get_user_activity/<userid>')
def get_user_activity(userid):
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("SELECT `log_id`, `violation_id`, m1.violationname, m2.violationname, s1.streetname, s2.streetname, `correct_incorrect`, `entry_date`,`sensitivity`,`duplicate_main_id`,`duplicated` FROM `user_log` INNER JOIN `violation_type` AS m1 ON m1.`violationtypeid` = `user_log`.`prev_violation` INNER JOIN `violation_type` AS m2 ON m2.`violationtypeid` = `user_log`.`updated_violation` INNER JOIN `street` AS s1 ON s1.`streetid` = `user_log`.`prev_street` INNER JOIN `street` AS s2 ON s2.`streetid` = `user_log`.`updated_street` WHERE `user_id` = "+str(userid)+" Order BY log_id DESC;")
    cursor.execute(query)
    for a, b, c, d, e, f, g, h, i, j, k in cursor:
        cor = "Correct"
        if g == 0:
            cor = "Incorrect"
        elif g == -1:
            cor = "-"
        if c == 'None':
            c = '-'
        if d == 'None':
            d = '-'
        if e == 'None':
            e = '-'
        if f == 'None':
            f = '-'
        if int(i)==0:
            i = '-'
        elif int(i) == 1:
            i = 'High'
        else:
            i = 'Low'

        if int(j) == 0:
            j = '-'
        if int(k) == 0:
            k = '-'
        elif int(k) == 1:
            k = 'Duplicated'
        else:
            k = 'Not Duplicated'
        data.append({
            "log_id": a,
            "violation_id": b,
            "prev_vio": c,
            "updated_vio": d,
            "prev_street": e,
            "updated_street": f,
            "cor": cor,
            "sensitivity": i,
            "main_id": j,
            "duplicated": k,
            "entry_date": h
        })
    cursor.close()
    cnx.close()
    return {'activity': data}


@app.route('/get_all_violation')
def get_all_violation():

    violation_table_data = list()

    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("SELECT violation.violation_id, violation.violation_type_id, violation_type.violationname, violation.street_id, street.streetname, violation.accurate, violation.risk, violation.violation_date, violation.violation_time, violation.correct, violation.device_id FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id INNER JOIN street ON street.streetid = violation.street_id WHERE violation.correct != -2 and violation.correct != 2 ORDER BY violation.violation_id DESC;")
    cursor.execute(query)

    for a, b, c, d, e, f, g, h, i, j, k in cursor:
        str = "Correct"
        if j == 0:
            str = "Incorrect"
        elif j == -1:
            str = "Pending"
        violation_table_data.append({
            "violation_id": a,
            "violation_type_id": b,
            "violation_name": c,
            "streetid": d,
            "street_name": e,

            "accurate": f,
            "risk": g,
            "violation_date": h.strftime('%b %d, %Y'),
            "violation_date_format": h.strftime('%Y-%m-%d'),
            "violation_time": i.strftime('%H:%M'),

            "cor": str,
            "dev_id": k
        })

    pages = math.floor(len(violation_table_data) / 10)
    if not (len(violation_table_data) % 10 == 0):
        pages = pages + 1

    cursor.close()
    cnx.close()
    vv = get_vio_for_verify()

    return {"myData": violation_table_data, "pages": pages, "vio": vv, "street_list": get_street_list()}


@app.route('/get_all_duplicate_violation')
def get_all_duplicate_violation():

    violation_table_data = list()

    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("SELECT violation.violation_id, violation.violation_type_id, violation_type.violationname, violation.street_id, street.streetname, violation.violation_date, violation.violation_time, violation.device_id, violation.super_violation_id FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id INNER JOIN street ON street.streetid = violation.street_id WHERE violation.correct=-2 ORDER BY violation.violation_id DESC;")
    cursor.execute(query)

    for a, b, c, d, e, f, g, h, i in cursor:
        temp = i.split(',')
        for lk in temp:
            if int(lk) != 0:
                violation_table_data.append({
                    "violation_id": a,
                    "violation_type_id": b,
                    "violation_name": c,
                    "streetid": d,
                    "street_name": e,
                    "violation_date": f.strftime('%b %d, %Y'),
                    "violation_date_format": f.strftime('%Y-%m-%d'),
                    "violation_time": g.strftime('%H:%M'),
                    "device_id": h,
                    "super_violation_id": int(lk),
                })

    pages = math.floor(len(violation_table_data) / 10)
    if not (len(violation_table_data) % 10 == 0):
        pages = pages + 1

    cursor.close()
    cnx.close()
    vv = get_vio_for_verify()

    return {"myData": violation_table_data, "pages": pages, "vio": vv}


@app.route('/get_single_violation_duplicate/<violation_id>/<main_id>')
def get_single_violation_duplicate(violation_id, main_id):

    violation_table_data = {'vio': {}, 'main': {}}
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
            "SELECT violation.violation_id, violation.violation_type_id, violation_type.violationname, violation.street_id, street.streetname, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation.lat, violation.long, violation.correct, violation.action_taken FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id INNER JOIN street ON street.streetid = violation.street_id WHERE violation.violation_id="+str(violation_id)+";")
    cursor.execute(query)
    for a, b, c, d, e, f, g, h, i, j, k, l, m, n in cursor:
        cs = "Not Reported"
        if n == 1:
            cs = "Reported"

        violation_table_data['vio']={
            "violation_id": a,
            "violation_type_id": b,
            "violation_name": c,
            "street_id": d,
            "street_name": e,
            "accurate": f,
            "risk": g,
            "display_img": h,
            "violation_date": i.strftime('%b %d, %Y'),
            "violation_time": j.strftime('%H:%M'),
            "lat": float(k),
            "lng": float(l),
            "correct": m,
            "current_status": cs,

            "new_violation_type_id": 0,
            "new_street_id": 0,
        }

    cursor.close()

    # #############################33
    cursor1 = cnx.cursor()
    query1 = (
            "SELECT violation.violation_id, violation.violation_type_id, violation_type.violationname, violation.street_id, street.streetname, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation.lat, violation.long, violation.correct, violation.action_taken FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id INNER JOIN street ON street.streetid = violation.street_id WHERE violation.violation_id=" + str(
        main_id) + ";")
    cursor1.execute(query1)
    for a, b, c, d, e, f, g, h, i, j, k, l, m, n in cursor1:
        cs = "Not Reported"
        if n == 1:
            cs = "Reported"

        violation_table_data['main'] = {
            "violation_id": a,
            "violation_type_id": b,
            "violation_name": c,
            "street_id": d,
            "street_name": e,
            "accurate": f,
            "risk": g,
            "display_img": h,
            "violation_date": i.strftime('%b %d, %Y'),
            "violation_time": j.strftime('%H:%M'),
            "lat": float(k),
            "lng": float(l),
            "correct": m,
            "current_status": cs,

            "new_violation_type_id": 0,
            "new_street_id": 0,
        }

    cursor1.close()
    # #################################3
    cnx.close()
    return violation_table_data


@app.route('/update_duplicate/<violation_id>/<main_id>/<duplicate>/<user_id>')
def update_duplicate(violation_id, main_id, duplicate, user_id):
    now = datetime.today()
    today_date = now.strftime("%Y-%m-%d")
    try:
        if int(duplicate) == 0:
            cnx = db_connection()
            temp = []
            cursor2 = cnx.cursor()
            query2 = (
                        "SELECT  `violation_id`,`super_violation_id` FROM `violation` WHERE `violation_id`='" + violation_id + "';")
            cursor2.execute(query2)
            for a, b in cursor2:
                temp = b.split(',')
            cursor2.close()
            super_ids = "0"
            for asw in temp:
                if int(asw) != 0 and int(main_id) != int(asw):
                    super_ids = super_ids+','+str(asw)
            query1 = ""
            if super_ids == "0":
                query1 = "UPDATE `violation` SET `correct`='-1',`super_violation_id`='0' WHERE `violation_id`='"+violation_id+"';"
            else:

                query1 ="UPDATE `violation` SET `super_violation_id`='"+super_ids+"' WHERE `violation_id`='" + violation_id + "';"

            cursor1 = cnx.cursor()
            query = ("INSERT INTO `user_log`( `user_id`, `violation_id`, `prev_violation`, `updated_violation`, `prev_street`, `updated_street`, `correct_incorrect`,`sensitivity`, `duplicate_main_id`, `duplicated`, `entry_date`) VALUES ('" + str(
                user_id) + "','" + str(violation_id) + "','0','0','0','0','-1','0','" + str(
                main_id) + "',-1,'" + today_date + "');")
            cursor1.execute(query1)
            cursor1.execute(query)
            cnx.commit()
            cursor1.close()
            cnx.close()
        else:
            cnx = db_connection()
            cursor1 = cnx.cursor()
            query1 = (
                        "UPDATE `violation` SET `correct`='2',`super_violation_id`='"+str(main_id)+"' WHERE `violation_id`='" + str(violation_id) + "';")
            cursor1.execute(query1)
            cnx.commit()
            query3 = ("INSERT INTO `user_log`( `user_id`, `violation_id`, `prev_violation`, `updated_violation`, `prev_street`, `updated_street`, `correct_incorrect`,`sensitivity`, `duplicate_main_id`, `duplicated`, `entry_date`) VALUES ('" + str(
                user_id) + "','" + str(violation_id) + "','0','0','0','0','-1','0','" + str(
                main_id) + "',1,'" + today_date + "');")
            cursor1.execute(query3)
            cnx.commit()
            cursor1.close()
            cnx.close()
        return {'result': 1}
    except Exception as e:
        print(e)
        return {'result': 0}


@app.route('/user_login', methods = ['POST'])
def user_login():
    request_data = request.get_json()
    user_login = {
        "userid": 0,
        "position": ""
    }
    username = str(request_data['username'])
    pwd = str(request_data['pwd'])

    cnx = db_connection()

    # #############################33
    cursor = cnx.cursor()
    query = ("SELECT `user_id`, `position` FROM `users` WHERE `username`='"+username+"' AND `pwd`='"+pwd+"';")
    cursor.execute(query)
    for a, b in cursor:
        user_login= {
            "userid": int(a),
            "position": b
        }

    cursor.close()
    cnx.close()
    return user_login


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1244)
