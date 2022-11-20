import time
import cv2
import base64
import requests
from requests import request



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
    "string_img":"",


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
    "display_img": "1.jpg",
    "violation_date": "2022-10-08",
    "violation_time": "14:30",
    "device_id": 0,
    "polygon_img": "",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },
{
    "lat": 24.64750,
    "long": 46.70259,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:13",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },

{
    "lat": 24.67188,
    "long": 46.69218,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },

{
    "lat": 24.67152,
    "long": 46.69241,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:10",
"string_img":"",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "device_id": 0,
    "polygon_img": "",
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
    "display_img": "1.jpg",
    "violation_time": "14:12",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:05",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,

    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },
{
    "lat": 24.63044,
    "long": 46.71588,
    "violation": "Median",
    "details": "Median",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:18",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:12",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:18",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },
{
    "lat": 24.67032,
    "long": 46.69339,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },
{
    "lat": 24.67032,
    "long": 46.69339,
    "violation": "Street Sweeping",
    "details": "Street Sweeping",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:28",
        "device_id": 0,
        "polygon_img": "",
    "violation_date": "2022-10-08",
"string_img":"",
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
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },
{
    "lat": 24.66984,
    "long": 46.69391,
    "violation": "Street Sweeping",
    "details": "Street Sweeping",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
"string_img":"",
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
        "display_img": "1.jpg",
        "violation_time": "14:28",
        "device_id": 0,
        "polygon_img": "",
        "violation_date": "2022-10-08",
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
    "lat": 24.66968,
    "long": 46.69409,
    "violation": "Rubble Source",
    "details": "Rubble Source",
    "accurate": 95,
    "risk": 2,
    "display_img": "1.jpg",
    "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
    "violation_date": "2022-10-08",
    "street_id": 0,
    "street_name": "",
    "violation_type_id": 0,
    "start_latlng": 0,
    "end_latlng": 0,
"string_img":"",
    },
    {
        "lat": 24.63173,
        "long": 46.71584,
        "violation": "Median",
        "details": "Median",
        "accurate": 95,
        "risk": 2,
        "display_img": "1.jpg",
        "violation_time": "14:28",
        "device_id": 0,
        "polygon_img": "",
        "violation_date": "2022-10-08",
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.66968,
        "long": 46.69409,
        "violation": "Street Sweeping",
        "details": "Street Sweeping",
        "display_img": "1.jpg",
        "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.63161,
        "long": 46.71588,
        "violation": "Median",
        "details": "Median",
        "display_img": "1.jpg",
        "violation_time": "14:28",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.64381,
        "long": 46.70303,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "1.jpg",
        "violation_time": "14:13",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
"string_img":"",
        "end_latlng": 0,
    },
{
        "lat": 24.70086,
        "long": 46.67760,
        "violation": "Street Sweeping",
        "details": "Street Sweeping",
        "display_img": "1.jpg",
        "violation_time": "14:06",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.64324,
        "long": 46.70308,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "1.jpg",
        "violation_time": "14:13",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.64306,
        "long": 46.70310,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "1.jpg",
        "violation_time": "14:13",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.62704,
        "long": 46.71216,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "1.jpg",
        "violation_time": "14:29",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.64289,
        "long": 46.70312,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "1.jpg",
        "violation_time": "14:13",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.62704,
        "long": 46.71216,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "1.jpg",
        "violation_time": "14:29",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.64273,
        "long": 46.70314,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "1.jpg",
        "violation_time": "14:13",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
"string_img":"",
        "end_latlng": 0,
    },
{
        "lat": 24.62679,
        "long": 46.71179,
        "violation": "Major Asphalt",
        "details": "Major Asphalt",
        "display_img": "1.jpg",
        "violation_time": "14:29",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.64220,
        "long": 46.70319,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "1.jpg",
        "violation_time": "14:13",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.62667,
        "long": 46.71159,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "1.jpg",
        "violation_time": "14:29",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.70381,
        "long": 46.67597,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "1.jpg",
        "violation_time": "14:05",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.62819,
        "long": 46.70886,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "44.jpg",
        "violation_time": "14:23",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.65328,
        "long": 46.70177,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "45.jpg",
        "violation_time": "14:12",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.63427,
        "long": 46.70392,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "46.jpg",
        "violation_time": "14:14",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.62507,
        "long": 46.70926,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "47.jpg",
        "violation_time": "14:19",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.63024,
        "long": 46.70724,
        "violation": "Minor Asphalt",
        "details": "Minor Asphalt",
        "display_img": "48.jpg",
        "violation_time": "14:25",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },

{
        "lat": 24.70680,
        "long": 46.67471,
        "violation": "Communication Tower",
        "details": "Communication Tower",
        "display_img": "49.jpg",
        "violation_time": "14:04",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.67365,
        "long": 46.69122,
        "violation": "Rubble Source",
        "details": "Rubble Source",
        "display_img": "50.jpg",
        "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.63150,
        "long": 46.70430,
        "violation": "Street Sweeping",
        "details": "Street Sweeping",
        "display_img": "51.jpg",
        "violation_time": "14:15",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.69054,
        "long": 46.68283,
        "violation": "Major Asphalt",
        "details": "Major Asphalt",
        "display_img": "52.jpg",
        "violation_time": "14:09",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.63144,
        "long": 46.70430,
        "violation": "Street Sweeping",
        "details": " Street Sweeping",
        "display_img": "54.jpg",
        "violation_time": "14:15",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.67348,
        "long": 46.69132,
        "violation": "Rubble Source",
        "details": " Rubble Source",
        "display_img": "55.jpg",
        "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.67330,
        "long": 46.69141,
        "violation": "Rubble Source",
        "details": " Rubble Source",
        "display_img": "56.jpg",
        "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.67312,
        "long": 46.69151,
        "violation": "Rubble Source",
        "details": " Rubble Source",
        "display_img": "57.jpg",
        "violation_time": "14:11",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
{
        "lat": 24.62819,
        "long": 46.70897,
        "violation": "Minor Asphalt",
        "details": " Minor Asphalt",
        "display_img": "58.jpg",
        "violation_time": "14:23",
    "device_id": 0,
    "polygon_img": "",
        "violation_date": "2022-10-08",
        "accurate": 95,
        "risk": 2,
        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,
        "start_latlng": 0,
        "end_latlng": 0,
"string_img":"",
    },
]

img = cv2.imread('to_upload_img/1.jpg')
string_img = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

tttttt = []
for vio in tett:
    temp = {
        "lat": float(vio['lat']),
        "long": float(vio['long']),
        "violation": vio['violation'],
        "details": vio['violation'],
        "accurate": 90,
        "risk": 00,
        "display_img": "1.jpg",
        "violation_date": "2022-10-08",
        "violation_time": "14:29",

        "device_id": 1,
        "polygon_img": "0",

        "street_id": 0,
        "street_name": "",
        "violation_type_id": 0,

        "string_img": string_img
    }
    tttttt.append(temp)

print("\nTimer Started!!")
x = time.perf_counter()
print("Processing Please Wait.............")
#pending = upload_dataset(tett)
re = requests.post("http://127.0.0.1:1255/upload_vio", json={'vio' : tttttt})
pending = re.json()['pending']

print("Processing Complete.")
print("\nResult Summary:")
print("\tTotal Violations: ", len(tttttt))
print("\tTime Consume in Sec: ", time.perf_counter() - x)
print("\tBusy Streets: ", len(pending))

