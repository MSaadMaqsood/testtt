import xlsxwriter

workbook = xlsxwriter.Workbook('Violations.xlsx')
worksheet = workbook.add_worksheet()


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
        
    },
]
cell_format = workbook.add_format({'bold': True})
head = ['Lat', 'Long', 'Violation Type', 'Details', 'Display img', 'Violation Time', 'Violation Date', 'Accurate', 'Risk']
worksheet.write_row(0, 0, head, cell_format)
worksheet.set_column(0, 6, 15)
for i in range(len(tett)):
    temp = []
    temp.append(tett[i]['lat'])
    temp.append(tett[i]['long'])
    temp.append(tett[i]['violation'])
    temp.append(tett[i]['details'])
    temp.append(tett[i]['display_img'])
    temp.append(tett[i]['violation_time'])
    temp.append(tett[i]['violation_date'])
    temp.append(tett[i]['accurate'])
    temp.append(tett[i]['risk'])

    worksheet.write_row(i+1, 0, temp)
workbook.close()