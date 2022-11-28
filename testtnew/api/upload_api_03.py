
from datetime import datetime
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

def side_check(lat1, lng1, lat2, lng2,test = 0):
    url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat1) + "," + str(lng1) + "&destination=" + str(lat2) + "," + str(lng2) + "&key=" + api_text
    response1 = requests.request("GET", url1, headers={}, data={})
    if len(response1.json()['routes'][0]['legs'][0]['steps']) == 1:

        return True
    else:
        lk = True

        for i in response1.json()['routes'][0]['legs'][0]['steps']:
            if i['html_instructions'].find('right') > -1 or i['html_instructions'].find('left') > -1 or i[
                'html_instructions'].find('Turn') > -1 or i['html_instructions'].find('turn') > -1:

                lk = False
                break
            try:
                if i["maneuver"].find('turn-right') > -1 or i["maneuver"].find('turn-left') > -1  or i["maneuver"].find('turn-sharp-left') > -1 or i["maneuver"].find('turn-sharp-right') > -1:
                    lk = False
                    break
            except:
                pass
        if lk:
            return True

        url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(lat2) + "," + str(
            lng2) + "&destination=" + str(lat1) + "," + str(lng1) + "&key=" + api_text
        response = requests.request("GET", url, headers={}, data={})
        if len(response.json()['routes'][0]['legs'][0]['steps']) == 1:

            return True

        else:


            for i in response.json()['routes'][0]['legs'][0]['steps']:
                if i['html_instructions'].find('right') > -1 or i['html_instructions'].find('left') > -1 or i['html_instructions'].find('Turn') > -1 or i['html_instructions'].find('turn') > -1:
                    return False
                try:
                    if i["maneuver"].find('turn-right') > -1 or i["maneuver"].find('turn-left') > -1 or i["maneuver"].find('turn-sharp-left') > -1 or i["maneuver"].find('turn-sharp-right') > -1:
                        return False
                except:
                    pass
            return True


def make_sec_point(lat1, lng1, lat2, lng2,):

    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+lat1+","+lng1+"&destination="+lat2+","+lng2+"&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    re = []
    if len(response.json()['routes'][0]['legs'][0]['steps']) == 1:
        #print("Google Map: ",response.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value'],", ","Calculated: ",calcCrow(float(lat1), float(lng1), float(lat2), float(lng2)))
        if abs(calcCrow(float(lat1), float(lng1), float(lat2), float(lng2)) - float(response.json()['routes'][0]['legs'][0]['steps'][0]['distance']['value'])) <= 1:
            re = [
                    {
                        "lat":float(lat1),
                        "lng": float(lng1),
                    },{
                        "lat": float(lat2),
                        "lng": float(lng2),
                    }
                ]
    return re


def get_second_latlng(lat, long):
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


def make_responce(latlng1, latlng2):
    qwe = {
        "starting":"",
        "ending": "",
        "polylines":[]
    }
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + latlng1 + "&destination=" + latlng2 + "&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})

    if len(response.json()['routes'][0]['legs'][0]['steps']) > 1:
        url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + latlng2 + "&destination=" + latlng1 + "&key=" + api_text
        response1 = requests.request("GET", url1, headers={}, data={})

        al = []

        l = polyline.decode(response1.json()["routes"][0]['overview_polyline']['points'])
        for i in l:
            temp = {'lat': i[0], 'lng': i[1]}
            al.append(temp)
        qwe = {
            "starting": latlng2,
            "ending": latlng1,
            "polylines": al
        }
    else:
        al = []
        l = polyline.decode(response.json()["routes"][0]['overview_polyline']['points'])
        for i in l:
            temp = {'lat': i[0], 'lng': i[1]}
            al.append(temp)
        qwe = {
            "starting": latlng1,
            "ending": latlng2,
            "polylines": al
        }
    return qwe


def update_make_responce(latlng1, latlng2):

    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+latlng1+"&destination="+latlng2+"&key=" + api_text
    response = requests.request("GET", url, headers={}, data={})
    if len(response.json()['routes'][0]['legs'][0]['steps']) > 1:
        url1 = "https://maps.googleapis.com/maps/api/directions/json?origin=" + latlng2 + "&destination=" + latlng1 + "&key=" + api_text
        response1 = requests.request("GET", url1, headers={}, data={})
        if len(response1.json()['routes'][0]['legs'][0]['steps']) > 1:
            return []
        else:
            al = []
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


def new_side(temp, test = 0):

    if len(temp) == 1:
        q = []
        z = get_second_latlng(temp[0]['lat'],temp[0]['lng'])
        if len(z) > 0:
            q.append(make_responce(str(z[0]['lat']) + "," + str(z[0]['lng']),
                                                  str(z[1]['lat']) + "," + str(z[1]['lng'])))
        else:
            q.append({"starting": str(temp[0]['lat'])+","+str(temp[0]['lng']),
            "ending": "0,0",
            "polylines":[]})

        return str(temp[0]['lat'])+","+str(temp[0]['lng']), str(temp[0]['lat'])+","+str(temp[0]['lng']), q
    elif len(temp) > 1:
        maxA= ""
        maxB = ""
        lines = []
        max_distance = 0
        max_distance_point_01 = 0
        max_distance_point_02 = 0
        for violation in range(len(temp)):
            for sec_vio in range(len(temp)):
                if violation == sec_vio:
                    continue
                dist = calcCrow(temp[violation]['lat'], temp[violation]['lng'],
                                temp[sec_vio]['lat'], temp[sec_vio]['lng'])
                if max_distance < dist:
                    max_distance = dist
                    max_distance_point_01 = violation
                    max_distance_point_02 = sec_vio

        maxA = str(temp[max_distance_point_01]['lat'])+","+str(temp[max_distance_point_01]['lng'])
        maxB = str(temp[max_distance_point_02]['lat']) + "," + str(temp[max_distance_point_02]['lng'])

        if max_distance <= 300:
            lines.append(make_responce(maxA, maxB))
        else:
            sorted_points = []
            sorted_points_dist = [{'point':max_distance_point_01, 'dist': 0}]
            sorted_points.append(max_distance_point_01)
            for count in range(len(temp) - 1):
                min_dis = 1000000000000000
                min_dist_point = 0
                for violation in range(len(temp)):
                    if violation == max_distance_point_01 or violation in sorted_points:
                        continue
                    dist = calcCrow(temp[violation]['lat'], temp[violation]['lng'],
                                    temp[max_distance_point_01]['lat'],
                                    temp[max_distance_point_01]['lng'])
                    if min_dis > dist:
                        min_dis = dist
                        min_dist_point = violation

                sorted_points.append(min_dist_point)
                sorted_points_dist.append({'point': min_dist_point, 'dist': min_dis})

            start_point = 0
            for mnb in range(1, len(temp)):
                if sorted_points_dist[mnb]['dist']-sorted_points_dist[mnb-1]['dist'] > 300:
                    if start_point == mnb-1:
                        #temp[sorted_points[start_point]]['lat']
                        z = get_second_latlng(temp[sorted_points[start_point]]['lat'], temp[sorted_points[start_point]]['lng'])
                        if len(z) > 0:
                            lines.append(make_responce(str(z[0]['lat']) + "," + str(z[0]['lng']),
                                                   str(z[1]['lat']) + "," + str(z[1]['lng'])))
                        else:
                            lines.append({"starting": str(temp[sorted_points[start_point]]['lat']) + "," + str(temp[sorted_points[start_point]]['lng']),
                                      "ending": "0,0",
                                      "polylines": []})
                        start_point = mnb
                    else:
                        # make polyline start point and mnb-1
                        lines.append(make_responce(
                            str(temp[sorted_points[start_point]]['lat']) + "," + str(temp[sorted_points[start_point]]['lng']),
                                     str(temp[sorted_points[mnb-1]]['lat']) + "," + str(temp[sorted_points[mnb-1]]['lng'])))
                        start_point = mnb
                if mnb == len(temp) - 1:
                    if start_point == mnb:
                        z = get_second_latlng(temp[sorted_points[start_point]]['lat'],
                                              temp[sorted_points[start_point]]['lng'])
                        if len(z) > 0:
                            lines.append(make_responce(str(z[0]['lat']) + "," + str(z[0]['lng']),
                                                       str(z[1]['lat']) + "," + str(z[1]['lng'])))
                        else:
                            lines.append({"starting": str(temp[sorted_points[start_point]]['lat']) + "," + str(
                                temp[sorted_points[start_point]]['lng']),
                                          "ending": "0,0",
                                          "polylines": []})

                    else:
                        # make polyline start point and mnb
                        lines.append(make_responce(
                            str(temp[sorted_points[start_point]]['lat']) + "," + str(
                                temp[sorted_points[start_point]]['lng']),
                            str(temp[sorted_points[mnb]]['lat']) + "," + str(temp[sorted_points[mnb]]['lng'])))

        return maxA, maxB, lines
    return "0,0","0,0",[]


def update_side(temp,prev):
    not_placed_point = []

    for vio in temp:
        placed = False

        for prev_vio in range(len(prev)):

            dist_A = calcCrow(vio['lat'], vio['lng'], float(prev[prev_vio]['starting'].split(',')[0]),
                              float(prev[prev_vio]['starting'].split(',')[1]))
            if not prev[prev_vio]['ending'] == "0,0":
                dist_B = calcCrow(vio['lat'], vio['lng'], float(prev[prev_vio]['ending'].split(',')[0]),
                                  float(prev[prev_vio]['ending'].split(',')[1]))
                dist_AB = calcCrow(float(prev[prev_vio]['starting'].split(',')[0]),
                                   float(prev[prev_vio]['starting'].split(',')[1]),
                                   float(prev[prev_vio]['ending'].split(',')[0]),
                                   float(prev[prev_vio]['ending'].split(',')[1]))

                if dist_A <= 300 or dist_B <= 300:

                    if dist_A >= dist_AB and dist_B <= 300:

                        xx = update_make_responce(prev[prev_vio]['starting'],
                                                             str(vio['lat']) + "," + str(vio['lng']))
                        if len(xx) > 0:
                            prev[prev_vio]['ending'] = str(vio['lat']) + "," + str(vio['lng'])
                            prev[prev_vio]['polylines'] = xx
                            placed = True
                    elif dist_B >= dist_AB and dist_A <= 300:
                        xx = update_make_responce(
                            str(vio['lat']) + "," + str(vio['lng']), prev[prev_vio]['ending'])
                        if len(xx) > 0:
                            prev[prev_vio]['starting'] = str(vio['lat']) + "," + str(vio['lng'])
                            prev[prev_vio]['polylines'] = xx
                            placed = True
                    elif abs(dist_AB - (dist_A + dist_B)) < 1:
                        placed = True
            else:
                if dist_A <= 300:
                    xx = update_make_responce(
                        prev[prev_vio]['starting'], str(vio['lat']) + "," + str(vio['lng']))
                    if len(xx) > 0:
                        placed = True
                        prev[prev_vio]['ending'] = str(vio['lat']) + "," + str(vio['lng'])
                        prev[prev_vio]['polylines'] = xx
            if placed:
                    break
        if not placed:
            not_placed_point.append(vio)
    if len(not_placed_point) > 0:
        a,b,c = new_side(not_placed_point)
        for i in c:
            prev.append(i)

    return prev



def main_function(list_of_all_violations, date_of_violation):
    list_of_ava_violations = []
    list_of_unava_violations = []
    list_of_incorrect_violations = []
    dict_of_violations_to_street = {}
    dict_of_trees_to_street = {}
    set_of_used_street_id = set()

    set_of_used_street_id.add(list_of_all_violations[0]['street_id'])

    set_of_unava_street_id = get_used_street_ids(set_of_used_street_id)
    set_of_street_ava_ids = set_of_used_street_id.difference(set_of_unava_street_id)

    for i in set_of_street_ava_ids:
        dict_of_violations_to_street[int(i)] = []
        dict_of_trees_to_street[int(i)] = []
    for violation in list_of_all_violations:
        if int(violation['street_id']) in set_of_unava_street_id:
            list_of_unava_violations.append(violation)
        else:
            list_of_ava_violations.append(violation)
            if int(violation['violation_type_id']) == 13:
                dict_of_trees_to_street[int(violation['street_id'])].append({'lat':violation['lat'],'lng':violation['long']})
            else:
                dict_of_violations_to_street[int(violation['street_id'])].append({'lat':violation['lat'],'lng':violation['long']})


    set_of_street_ava_ids = set_of_used_street_id.difference(set_of_unava_street_id)

    if len(set_of_street_ava_ids) > 0:
        update_street_status(set_of_street_ava_ids, 1)

    # #########

    for street in set_of_street_ava_ids:

        temp = dict_of_violations_to_street[street]
        ref_pointa, ref_pointb, prev_point_one, prev_point_two, total_violation = get_prev_violations_StreetID(street,
                                                                                                               date_of_violation)

        if int(total_violation) > 0:
            # update
            total_violation = int(total_violation) + len(temp)
            side1 = []
            side2 = []
            for i in range(len(temp)):
                if side_check(temp[i]['lat'], temp[i]['lng'], ref_pointa['min'].split(',')[0],
                              ref_pointa['min'].split(',')[1]):
                    side1.append(temp[i])
                elif side_check(temp[i]['lat'], temp[i]['lng'], ref_pointa['max'].split(',')[0],
                                ref_pointa['max'].split(',')[1]):
                    side1.append(temp[i])
                else:
                    side2.append(temp[i])
            lines01 = update_side(side1, prev_point_one)
            lines02 = update_side(side2, prev_point_two)
            update_map_view(str(street), str(lines01), str(lines02), str(total_violation), date_of_violation)
        elif len(temp) > 0:
            if len(temp) == 1:
                lines = []
                z = get_second_latlng(temp[0]['lat'], temp[0]['lng'])
                if len(z) > 0:
                    lines.append(make_responce(str(z[0]['lat']) + "," + str(z[0]['lng']),
                                               str(z[1]['lat']) + "," + str(z[1]['lng'])))
                else:
                    lines.append({'starting': str(temp[0]['lat']) + "," + str(
                        temp[0]['lng']),
                                  'ending': '0,0',
                                  'polylines': []})
                insert_map_view(street, date_of_violation, {'min': str(z[0]['lat']) + "," + str(z[0]['lng']),
                                                            'max': str(z[0]['lat']) + "," + str(z[0]['lng'])},
                                {'min': 0, 'max': 0}, lines, [], 1)
            else:
                side1 = []
                side2 = []
                side1.append(temp[0])

                for i in range(1, len(temp)):
                    if side_check(temp[0]['lat'], temp[0]['lng'], temp[i]['lat'], temp[i]['lng']):
                        side1.append(temp[i])
                    else:
                        side2.append(temp[i])
                side1_ref1, side1_ref2, side1_ = new_side(side1)
                side2_ref1, side2_ref2, side2_ = new_side(side2)

                insert_map_view(street, date_of_violation, {'min': side1_ref1, 'max': side1_ref2},
                                {'min': side2_ref1, 'max': side2_ref2}, side1_, side2_, len(temp))

    ####### Treeeeee

    for street in set_of_street_ava_ids:
        temp = dict_of_trees_to_street[street]
        ref_pointa, ref_pointb, prev_point_one, prev_point_two, total_violation = get_prev_violations_tree_StreetID(
            street, date_of_violation)

        if int(total_violation) > 0:
            # update
            total_violation = int(total_violation) + len(temp)
            side1 = []
            side2 = []
            for i in range(len(temp)):
                if side_check(temp[i]['lat'], temp[i]['lng'], ref_pointa['min'].split(',')[0],
                              ref_pointa['min'].split(',')[1]):
                    side1.append(temp[i])
                elif side_check(temp[i]['lat'], temp[i]['lng'], ref_pointa['max'].split(',')[0],
                                ref_pointa['max'].split(',')[1]):
                    side1.append(temp[i])
                else:
                    side2.append(temp[i])
            lines01 = update_side(side1, prev_point_one)
            lines02 = update_side(side2, prev_point_two)
            update_map_view_tree(str(street), str(lines01), str(lines02), str(total_violation), date_of_violation)
        elif len(temp) > 0:
            if len(temp) == 1:
                lines = []
                z = get_second_latlng(temp[0]['lat'], temp[0]['lng'])
                if len(z) > 0:
                    lines.append(make_responce(str(z[0]['lat']) + "," + str(z[0]['lng']),
                                               str(z[1]['lat']) + "," + str(z[1]['lng'])))
                else:
                    lines.append({'starting': str(temp[0]['lat']) + "," + str(
                        temp[0]['lng']),
                                  'ending': '0,0',
                                  'polylines': []})
                insert_map_view_tree(street, date_of_violation, {'min': str(z[0]['lat']) + "," + str(z[0]['lng']),
                                                                 'max': str(z[0]['lat']) + "," + str(z[0]['lng'])},
                                     {'min': 0, 'max': 0}, lines, [], 1)
            else:
                side1 = []
                side2 = []
                side1.append(temp[0])
                for i in range(1, len(temp)):
                    if side_check(temp[0]['lat'], temp[0]['lng'], temp[i]['lat'], temp[i]['lng']):
                        side1.append(temp[i])
                    else:
                        side2.append(temp[i])
                side1_ref1, side1_ref2, side1_ = new_side(side1)
                side2_ref1, side2_ref2, side2_ = new_side(side2)

                insert_map_view_tree(street, date_of_violation, {'min': side1_ref1, 'max': side1_ref2},
                                     {'min': side2_ref1, 'max': side2_ref2}, side1_, side2_, len(temp))


    if len(set_of_street_ava_ids) > 0:
        update_street_status(set_of_street_ava_ids, 0)

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