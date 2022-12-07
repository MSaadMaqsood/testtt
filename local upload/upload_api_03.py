from datetime import datetime, timedelta
import requests
import math
import mysql.connector
import json
import ast
import polyline
import time
from flask import Flask
from flask import request
from flask_cors import CORS
from basic_func import *
import sys


def set_street_id_name_viotype_correct_to_violations(list_of_all_violations):
    set_of_used_street_id = set()
    list_of_all_streets = get_list_of_streets()
    list_of_violations_type = get_list_of_all_violations()
    list_of_violation = []
    list_of_incorrect_violation = []
    for vio in range(len(list_of_all_violations)):
        temp_name = get_street_name(
            list_of_all_violations[vio]['lat'], list_of_all_violations[vio]['lng'])
        list_of_all_violations[vio]['street_name'] = temp_name
        list_of_all_violations[vio]['street_id'] = 0
        list_of_all_violations[vio]['violation_type_id'] = 0
        for i in list_of_violations_type:
            if list_of_all_violations[vio]['violation'] == i['violationname']:
                list_of_all_violations[vio]['violation_type_id'] = i['violationtypeid']
        if temp_name != "Unknown road":

            for street in list_of_all_streets:
                if street['name'] == temp_name:
                    list_of_all_violations[vio]['street_id'] = int(
                        street['id'])
                    break
            if list_of_all_violations[vio]['street_id'] == 0:
                list_of_all_violations[vio]['street_id'] = upload_new_street_name(
                    temp_name)
                list_of_all_streets.append({
                    'id': list_of_all_violations[vio]['street_id'],
                    'name': temp_name
                })
        set_of_used_street_id.add(int(list_of_all_violations[vio]['street_id']))
        list_of_all_violations[vio]['correct'] = -1
        list_of_violation.append(list_of_all_violations[vio])
    #print(list_of_violation)
    return list_of_violation, list_of_incorrect_violation, set_of_used_street_id


def get_prev_violation_last_3_day(str_id, udate):

    d1 = datetime.strptime(udate, "%Y-%m-%d")
    d = d1 - timedelta(days=3)
    data = []
    cnx = db_connection()
    cursor = cnx.cursor()
    query = ("SELECT `violation_id`,`violation_type_id`,`lat`,`long` FROM `violation` WHERE street_id='" +
             str(str_id)+"' AND violation_date BETWEEN '"+d.strftime('%Y-%m-%d')+"' AND '"+udate+"' AND correct='1';")
    cursor.execute(query)
    for a, b, c, d in cursor:
        data.append({
            "vio_id": a,
            "type_id": b,
            "lat": c,
            "lng": d
        })
    cursor.close()
    cnx.close()

    return data


def main_function(list_of_all_violations, date_of_violation):
    list_of_ava_violations = []
    list_of_unava_violations = []
    list_of_incorrect_violations = []
    dict_of_violations_to_street = {}
    dict_of_Prev_violations_to_street = {}
    dict_of_trees_to_street = {}
    count_of_tree = 0
    # print(list_of_all_violations)
    list_of_all_violations, list_of_incorrect_violations, set_of_used_street_id = set_street_id_name_viotype_correct_to_violations(
        list_of_all_violations)

    #set_of_unava_street_id = get_used_street_ids(set_of_used_street_id)
    set_of_street_ava_ids = set_of_used_street_id
    for i in set_of_street_ava_ids:
        dict_of_violations_to_street[int(i)] = []
        dict_of_trees_to_street[int(i)] = []
    for violation in list_of_all_violations:

        list_of_ava_violations.append(violation)
        if (violation['violation_type_id']) == 13:
            count_of_tree = count_of_tree + 1
            dict_of_trees_to_street[(violation['street_id'])].append(
                {'lat': violation['lat'], 'lng': violation['lng']})
        else:
            #print(violation)
            dict_of_violations_to_street[(violation['street_id'])].append(
                {'lat': violation['lat'], 'lng': violation['lng']})



    print("Total Streets: ", len(set_of_used_street_id))
    print("")
    print("Number of Trees: ", count_of_tree)
    print("Number of others violations: ", len(
        list_of_ava_violations)-count_of_tree)
    print("")
    # if len(set_of_street_ava_ids) > 0:
    ##update_street_status(set_of_street_ava_ids, 1)

    # #########

    for i in set_of_street_ava_ids:
        dict_of_Prev_violations_to_street[int(i)] = get_prev_violation_last_3_day(
            int(i), date_of_violation)
    for i in range(len(list_of_ava_violations)):
        if list_of_ava_violations[i]['street_id'] != 0 and int(list_of_ava_violations[i]['violation_type_id']) != 0:
            super_ids = "0"
            for j in dict_of_Prev_violations_to_street[int(list_of_ava_violations[i]['street_id'])]:
                dddd = calcCrow(float(list_of_ava_violations[i]['lat']), float(list_of_ava_violations[i]['lng']),
                                float(j['lat']), float(j['lng']))
                print(dddd)
                if dddd < 200 and int(list_of_ava_violations[i]['violation_type_id']) == int(j['type_id']):
                    print("superrrrrr")
                    super_ids = super_ids+","+str(j['vio_id'])
                    list_of_ava_violations[i]['correct'] = -2

            list_of_ava_violations[i]['super_violation_id'] = super_ids
    if len(list_of_ava_violations) > 0:
        insert_violations_Street(list_of_ava_violations)


    return list_of_unava_violations


# {
#         "street_id": 0,
#         "street_name": "",
#
#         "violation_type_id": 0,
#         "violation": "",
#
#         "details": "",
#         "accurate": 0,
#         "risk": 0,
#         "display_img": "",
#         "string_img": "",
#
#         "lat": 0.0,
#         "long": 0.0,
#
#         "device_id": 0,
#         "polygon_img": "",
#
#         "violation_date": "",
#         "violation_time": "",
#
#         "correct": -1
#     }


# x = {
#     'streetid': 0,
#     'side01_ref': {'start_point': 0.0, 'end_point': 0.0},
#     'side02_ref': {'start_point': 0.0, 'end_point': 0.0},
#     'side01': [
#                 {'start_point': 0.0, 'end_point': 0.0, 'points': ["0.0,0.0"], 'distance':0, polyline:[]}
#     ],
#     'side02': [
#                 {'start_point': 0.0, 'end_point': 0.0, 'points': ["0.0,0.0"], 'distance':0, polyline:[]}
#     ],
#     'upload_date': "",
#     'total_violations': 0
# }
