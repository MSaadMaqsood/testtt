import math
from select import select
from flask import Flask, jsonify, render_template
from numpy import insert
from requests import request
import mysql.connector
from flask import request
from flask_cors import CORS
from datetime import datetime
from flask import send_file
from datetime import datetime, timedelta
from google_api import *
from pdfmaker import *
from collections import Counter

app = Flask(__name__)
CORS(app)


def db_connection():
    host = 'localhost'
    user = "root"
    password = ""
    database = 'elm'
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
    return cnx


@app.route('/show_violation_image/<image_name>')
def show_violation_image(image_name):
    filename = image_name
    filepath = "./images/"+filename
    return send_file(filepath, mimetype='image/gif')


@app.route('/getpdf/<pdf_name>')
def getpdf(pdf_name):
    filename = pdf_name
    filepath = "./pdf/"+filename
    return send_file(filepath)


"""################################### Dashboard ######################################################"""


@app.route('/get_dashboard')
def get_dashboard():
    data_map = violation_map_data()
    return jsonify({"street_health": 95, "green_index": 95, "risk": 95, "data_map": data_map})


def violation_map_data():
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = (
                "SELECT `violation_id`, `street_id`, `lat`, `long` FROM `violation` WHERE `violation_date` = '2022-09-29' OR `violation_date` = '2022-09-30' ORDER By `street_id`,`violation_id` ASC;")
    cursor.execute(query)
    prev_id = 1
    temp = []
    temp_bool = False
    for a, b, c, d in cursor:
        if not b == prev_id:
            if temp_bool:
                data.append(temp)
                temp = []
            else:
                temp_bool = True
        temp.append({
            "id": a,
            "street_id": b,
            "lat": float(c),
            "long": float(d),
        })
        prev_id = b
    data.append(temp)
    cursor.close()
    cnx.close()

    used = []
    list_for_circle = []
    for i in data:
        ignore = []
        for j in i:
            make = False
            if j['id'] in ignore:
                continue
            for k in i:
                if j['id'] == k['id']:
                    continue
                dist = get_distance_btw_violation_by_distance_matrix_api(k['lat'], k['long'], j['lat'], j['long'])
                if dist < 350 and dist != 0:
                    ignore.append(k['id'])
                    used.append([
                                {
                                    "street_id": k['street_id'],
                                    "lat": k['lat'],
                                    "lng": k['long'],
                                },{
                                    "street_id": k['street_id'],
                                    "lat": j['lat'],
                                    "lng": j['long'],
                                },
                        ]
                    )
                    make = True
            if not make:
                list_for_circle.append({"street_id": j['street_id'],
                                    "lat": j['lat'],
                                    "lng": j['long'],})
                #re = get_second_latlng_for_single_violation_by_direction_api(j['lat'], j['long'], j['street_id'])
                #if len(re) > 0:
                #    used.append(re)

    return {'line':used,'circle':list_for_circle}


"""################################### Violation Page ######################################################"""


@app.route('/get_violation_page/<street_id>')
def get_violation_page(street_id):
    street_ls, street_nm = get_street_list(street_id)
    violation_table, violation_count = get_violation_table_now_default(street_id)
    return jsonify({
        "street_name": street_nm,
        "street_health": get_street_health(street_id, violation_count),
        "violation_table": violation_table,
        "list_of_streets": street_ls
    })


def get_street_health(street_id, violation_count):
    Asphalt = Sidewalk = Lighting = Cleanliness = Afforestation = Fossils = 100
    violation_count.sort()
    c = Counter(violation_count)
    a = list(c.keys())
    b = list(c.values())
    print(a, b)
    for i in range(len(a)):
        match int(a[i]):
            case 1:
                Asphalt = Asphalt - b[i] * 3
                if Asphalt < 0:
                    Asphalt = 0
                continue
            case 2:
                Sidewalk = 100 - b[i] * 2
                print(Sidewalk, b[i])
                if Sidewalk < 0:
                    Sidewalk = 0
                continue
            case 3:
                Lighting = 100 - b[i] * 2
                if Lighting < 0:
                    Lighting = 0
                continue
            case 4:
                Cleanliness = 100 - b[i] * 2
                if Cleanliness < 0:
                    Cleanliness = 0
                continue
            case 5:
                Afforestation = 100 - b[i] * 2
                if Afforestation < 0:
                    Afforestation = 0
                continue
            case 6:
                Fossils = 100 - b[i] * 2
                if Fossils < 0:
                    Fossils = 0
                continue
            case 7:
                Asphalt = Asphalt - b[i] * 6
                if Asphalt < 0:
                    Asphalt = 0
                continue
    green_index = int((Asphalt+Sidewalk+Lighting+Cleanliness+Afforestation+Fossils)/6)
    return {
                "street_risk_rate": 100-green_index,
                "green_index": green_index,
                "Asphalt": Asphalt,
                "Sidewalk": Sidewalk,
                "Lighting": Lighting,
                "Cleanliness": Cleanliness,
                "Afforestation": Afforestation,
                "Fossils": Fossils
            }


def get_street_list(street_id):
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
    query = ("SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.street_id=" + str(
        street_id) + " AND violation.violation_date='"+today_date+"';")

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
    return {"myData": violation_table_data, "pages": pages},violation_count_list


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
            "SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.street_id=" + str(
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
    return {"myData": violation_table_data, "pages": pages}


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
            "status": "Not Reported"
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
            "status": st
        }
        print(i,j,st)
    cursor.close()
    cnx.close()
    return violation_table_data


@app.route('/export_violation_pdf', methods = ['POST'])
def export_dashboard_csv():

    x = request.get_json()
    print(x['violation_table_data'])
    pdf_name = pdf_maker(x['street_name'], x['street_info'], x['violation_date'], x['violation_table_data']['myData'])
    return {"pdf_name": pdf_name}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1151)
