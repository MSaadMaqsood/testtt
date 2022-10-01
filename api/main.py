from select import select
from flask import Flask, jsonify,render_template
from numpy import insert
from requests import request
import mysql.connector
from flask import request
from flask_cors import CORS
from datetime import datetime
from flask import send_file
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

def dBconnection():
    host = 'localhost'
    user = "root"
    password = ""
    database = 'elm'
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
    return cnx

@app.route('/showviolationimage/<imagename>')
def showviolationimage(imagename):
    filename = imagename
    filepath = "./images/"+filename
    return send_file(filepath, mimetype='image/gif')


@app.route('/get_violations/<streetid>')
def get_getVerifier(streetid):
    data = []
    data1 = []
    cnx = dBconnection()
    cursor = cnx.cursor()
    query = ("SELECT violation.violation_id,violation.violation_type_id, violation.accurate, violation.risk, violation.display_img, violation.violation_date, violation.violation_time, violation_type.violationname FROM violation INNER JOIN violation_type ON violation_type.violationtypeid = violation.violation_type_id WHERE violation.street_id="+str(streetid)+" AND violation.violation_status='0';")
    cursor.execute(query)

    for a, b, c, d, e, f, g, h in cursor:

        data.append({
            "violation_id": a,
            "violation_type_id": b,
            "accurate": c,
            "risk": d,
            "display_img": e,
            "violation_date": f.strftime('%b %d, %Y'),
            "violation_time": g.strftime('%H:%M'),
            "violation_name": h
        })
    cursor.close()
    cnx.close()

    print(data)
    return jsonify({"myData": data, "pages": 2})


@app.route('/get_all_violations_loc_list')


def get_all_violations_loc_list():
    data = []

    cnx = dBconnection()
    cursor = cnx.cursor()
    query = (
        "SELECT `street_id`,`start_lat`, `start_long`, `end_lat`, `end_long` FROM `violation` WHERE violation_status=0; ")
    cursor.execute(query)

    for a, b, c, d, e in cursor:
        data1 = []
        data1.append({
            "devid": a,
            "lat": float(b),
            "lng": float(c),
        })
        data1.append({
            "devid": a,
            "lat": float(d),
            "lng": float(e),
        })

        data.append(data1)
    cursor.close()
    cnx.close()
    return jsonify({"myData": data})


@app.route('/get_dashboard')
def get_dashboard():
    return jsonify({"street_health": 95, "green_index": 95, "risk": 95})


@app.route('/get_violation_page/<streetid>')
def get_violation_page(streetid):
    street = {"street_id": 1, "street_name": "ABC", "street_risk_rate": 5, "green_index": 95}
    street_health = {"Asphalt": 40, "Sidewalk": 60, "Lighting": 71, "Cleanliness": 90, "Afforestation": 95, "Fossils": 92}
    list_of_streets = [
        {"street_id": 1, "street_name": "street_1"},
        {"street_id": 2, "street_name": "street_2"},
        {"street_id": 3, "street_name": "street_3"},
        {"street_id": 4, "street_name": "street_4"},
        {"street_id": 5, "street_name": "street_5"},
        {"street_id": 6, "street_name": "street_6"},
        {"street_id": 7, "street_name": "street_7"},
        {"street_id": 8, "street_name": "street_8"},
    ]
    return jsonify({"street": street, "street_health": street_health, "list_of_streets": list_of_streets})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1151)