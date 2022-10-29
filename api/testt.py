# list_of_street_names = [{
#                             'violation':[
#                                             {
#                                                 'lat': 0,
#                                                 'long': 0,
#                                             }
#                             ],
#                             'side01':[],
#                             'side02':[],
#                             'total_violations':0,
#                             'ref':"",
#                             'date':''
#                     }
#                 ]
#
# for street in list_of_street_names:
#
#     street['ref'] = str(street['violation'][0]['lat'])+","+ str(street['violation'][0]['long'])
#     street['total_violations'] = len(street['violation'])
#
#     if len(street['violation']) > 1:
#         point_one = []
#         point_two = []
#         point_one.append(street['violation'][0])
#         for violation in range(1, len(street['violation'])):
#             if get_distance_btw_violation_by_distance_matrix_api(street['violation'][0]['lat'],
#                                                                  street['violation'][0]['long'],
#                                                                  street['violation'][violation]['lat'],
#                                                                  street['violation'][violation]['long']):
#                 point_one.append(street['violation'][violation])
#             else:
#                 point_two.append(street['violation'][violation])
#         if len(point_one) > 1:
#             max_distance = 0
#             max_distance_point_01 = 0
#             max_distance_point_02 = 0
#             for violation in range(len(point_one)):
#                 for sec_vio in range(len(point_one)):
#                     if violation == sec_vio:
#                         continue
#                     dist = calcCrow(point_one[violation]['lat'], point_one[violation]['long'],
#                                     point_one[sec_vio]['lat'], point_one[sec_vio]['long'])
#                     if max_distance < dist:
#                         max_distance = dist
#                         max_distance_point_01 = violation
#                         max_distance_point_02 = sec_vio
#             if max_distance <= 300:
#                 temp = {
#                     'start_latlng': str(point_one[max_distance_point_01]['lat']) + "," + str(point_one[max_distance_point_01]['long']),
#                     'end_latlng': str(point_one[max_distance_point_02]['lat']) + "," + str(point_one[max_distance_point_02]['long'])
#                 }
#                 street['side01'].append(temp)
#
#             else:
#                 sorted_points = []
#                 sorted_points.append(max_distance_point_01)
#                 for count in range(len(point_one) - 1):
#                     min_dis = 1000000000000000
#                     min_dist_point = 0
#                     for violation in range(len(point_one)):
#                         if violation == max_distance_point_01 or violation in sorted_points:
#                             continue
#                         dist = calcCrow(point_one[violation]['lat'], point_one[violation]['long'],
#                                         point_one[max_distance_point_01]['lat'],
#                                         point_one[max_distance_point_01]['long'])
#                         if min_dis > dist:
#                             min_dis = dist
#                             min_dist_point = violation
#
#                     sorted_points.append(min_dist_point)
#                 start_point = 0
#                 last_point = -1
#                 point = 0
#                 while point < len(sorted_points) - 1:
#                     dist = calcCrow(point_one[sorted_points[point]]['lat'], point_one[sorted_points[point]]['long'],
#                                     point_one[sorted_points[point + 1]]['lat'],
#                                     point_one[sorted_points[point + 1]]['long'])
#                     if dist <= 300:
#                         last_point = point + 1
#                     else:
#                         if last_point == -1:
#                             got_sec = get_second_latlng_for_single_violation_by_direction_api(
#                                 point_one[sorted_points[start_point]]['lat'],
#                                 point_one[sorted_points[start_point]]['long'])
#                             if len(got_sec) == 2:
#
#                                 temp = {
#                                     'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
#                                     'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng'])
#                                 }
#                                 street['side01'].append(temp)
#
#                             else:
#                                 temp = {
#                                     'start_latlng': str(point_one[sorted_points[start_point]]['lat']) + "," + str(point_one[sorted_points[start_point]]['long']),
#                                     'end_latlng': "0,0"
#                                 }
#                                 street['side01'].append(temp)
#
#                             start_point = start_point + 1
#                         else:
#                             temp = {
#                                 'start_latlng': str(point_one[sorted_points[start_point]]['lat']) + "," + str(
#                                 point_one[sorted_points[start_point]]['long']),
#                                 'end_latlng':  str(point_one[sorted_points[last_point]]['lat']) + "," + str(
#                                 point_one[sorted_points[last_point]]['long'])
#                             }
#                             street['side01'].append(temp)
#
#                             start_point = last_point + 1
#                             last_point = -1
#                     point = point + 1
#
#         else:
#             # point_one[0]['start_latlng'] = str(point_one[0]['lat'])+","+str(point_one[0]['long'])
#             # point_one[0]['end_latlng'] = "0"
#             got_sec = get_second_latlng_for_single_violation_by_direction_api(
#                 point_one[0]['lat'], point_one[0]['long'])
#             if len(got_sec) == 2:
#                 temp = {
#                     'start_latlng':str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
#                     'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng'])
#                 }
#                 street['side01'].append(temp)
#
#             else:
#                 temp = {
#                     'start_latlng': str(point_one[0]['lat']) + "," + str(point_one[0]['long']),
#                     'end_latlng': "0,0"
#                 }
#                 street['side01'].append(temp)
#
#         if len(point_two) > 1:
#             max_distance = 0
#             max_distance_point_01 = 0
#             max_distance_point_02 = 0
#             for violation in range(len(point_two)):
#                 for sec_vio in range(len(point_two)):
#                     if violation == sec_vio:
#                         continue
#                     dist = calcCrow(point_two[violation]['lat'], point_two[violation]['long'],
#                                     point_two[sec_vio]['lat'],
#                                     point_two[sec_vio]['long'])
#                     if max_distance < dist:
#                         max_distance = dist
#                         max_distance_point_01 = violation
#                         max_distance_point_02 = sec_vio
#             if max_distance <= 300:
#                 temp = {
#                     'start_latlng': str(
#                     point_two[max_distance_point_01]['lat']) + "," + str(
#                     point_two[max_distance_point_01]['long']),
#                     'end_latlng': str(
#                     point_two[max_distance_point_02]['lat']) + "," + str(
#                     point_two[max_distance_point_02]['long'])
#                 }
#                 street['side02'].append(temp)
#
#             else:
#                 sorted_points = []
#                 sorted_points.append(max_distance_point_01)
#                 for count in range(len(point_two) - 1):
#                     min_dis = 1000000000000000
#                     min_dist_point = 0
#                     for violation in range(len(point_two)):
#                         if violation == max_distance_point_01 or violation in sorted_points:
#                             continue
#                         dist = calcCrow(point_two[violation]['lat'], point_two[violation]['long'],
#                                         point_two[max_distance_point_01]['lat'],
#                                         point_two[max_distance_point_01]['long'])
#                         if min_dis > dist:
#                             min_dis = dist
#                             min_dist_point = violation
#
#                     sorted_points.append(min_dist_point)
#                 start_point = 0
#                 last_point = -1
#                 point = 0
#                 while point < len(sorted_points) - 1:
#                     dist = calcCrow(point_two[sorted_points[point]]['lat'], point_two[sorted_points[point]]['long'],
#                                     point_two[sorted_points[point + 1]]['lat'],
#                                     point_two[sorted_points[point + 1]]['long'])
#                     if dist <= 300:
#                         last_point = point + 1
#                     else:
#                         if last_point == -1:
#                             # point_two[sorted_points[start_point]]['start_latlng'] = str(
#                             #     point_two[sorted_points[start_point]]['lat']) + "," + str(
#                             #     point_two[sorted_points[start_point]]['long'])
#                             got_sec = get_second_latlng_for_single_violation_by_direction_api(
#                                 point_two[sorted_points[start_point]]['lat'],
#                                 point_two[sorted_points[start_point]]['long'])
#                             if len(got_sec) == 2:
#                                 temp = {
#                                     'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
#                                     'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng'])
#                                 }
#                                 street['side02'].append(temp)
#
#
#                             else:
#                                 temp = {
#                                     'start_latlng': str(point_two[sorted_points[start_point]]['lat']) + "," + str(
#                                     point_two[sorted_points[start_point]]['long']),
#                                     'end_latlng': "0,0"
#                                 }
#                                 street['side02'].append(temp)
#
#                             start_point = start_point + 1
#                         else:
#                             temp = {
#                                 'start_latlng': str(
#                                 point_two[sorted_points[start_point]]['lat']) + "," + str(
#                                 point_two[sorted_points[start_point]]['long']),
#                                 'end_latlng': str(
#                                 point_two[sorted_points[last_point]]['lat']) + "," + str(
#                                 point_two[sorted_points[last_point]]['long'])
#                             }
#                             street['side02'].append(temp)
#
#
#                             start_point = last_point + 1
#                             last_point = -1
#                     point = point + 1
#
#
#         elif len(point_two) == 1:
#
#             got_sec = get_second_latlng_for_single_violation_by_direction_api(
#                 point_two[0]['lat'], point_two[0]['long'])
#
#
#
#             if len(got_sec) == 2:
#
#                 temp = {
#                     'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
#                     'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng'])
#                 }
#                 street['side02'].append(temp)
#
#             else:
#                 temp = {
#                     'start_latlng': str(point_two[0]['lat']) + "," + str(point_two[0]['long']),
#                     'end_latlng': "0,0"
#                 }
#                 street['side02'].append(temp)
#
#
#     else:
#
#         got_sec = get_second_latlng_for_single_violation_by_direction_api(
#             street['violation'][0]['lat'], street['violation'][0]['long'])
#
#         if len(got_sec) == 2:
#             temp = {
#                 'start_latlng': str(got_sec[0]['lat']) + "," + str(got_sec[0]['lng']),
#                 'end_latlng': str(got_sec[1]['lat']) + "," + str(got_sec[1]['lng'])
#             }
#             street['side01'].append(temp)
#
#         else:
#             temp = {
#                 'start_latlng':str(street['violation'][0]['lat']) + "," + str(street['violation'][0]['long']),
#                 'end_latlng': "0,0"
#             }
#             street['side01'].append(temp)
#
#

# l = [{'street_id': 1, 'street_name': 'King Fahad Branch Rd', 'violation': [{'lat': 24.63427, 'long': 46.70392, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '46.jpg', 'violation_time': '14:14', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 1, 'street_name': 'King Fahad Branch Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.63144, 'long': 46.7043, 'violation': 'Street Sweeping', 'details': ' Street Sweeping', 'display_img': '54.jpg', 'violation_time': '14:15', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 1, 'street_name': 'King Fahad Branch Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.63427,46.70392', 'end_latlng': '24.63387,46.70392'}], 'side02': [], 'total_violations': 2, 'ref': '24.63427,46.70392', 'date': ''}, {'street_id': 5, 'street_name': 'Al Madina Al Munawwarah Rd', 'violation': [{'lat': 24.62503, 'long': 46.7092, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '1.jpg', 'violation_date': '2022-10-08', 'violation_time': '14:29', 'device_id': 0, 'polygon_img': '', 'street_id': 5, 'street_name': 'Al Madina Al Munawwarah Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.62488, 'long': 46.70893, 'violation': 'Major Asphalt', 'details': 'Major Asphalt', 'accurate': 7, 'risk': 6, 'display_img': '2.jpg', 'violation_date': '2022-10-08', 'violation_time': '14:30', 'street_id': 5, 'street_name': 'Al Madina Al Munawwarah Rd', 'violation_type_id': 7, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.62704, 'long': 46.71216, 'violation': 'Minor Asphalt', 'details': 'Minor Asphalt', 'display_img': '36.jpg', 'violation_time': '14:29', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 5, 'street_name': 'Al Madina Al Munawwarah Rd', 'violation_type_id': 1, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.62704, 'long': 46.71216, 'violation': 'Minor Asphalt', 'details': 'Minor Asphalt', 'display_img': '38.jpg', 'violation_time': '14:29', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 5, 'street_name': 'Al Madina Al Munawwarah Rd', 'violation_type_id': 1, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.62679, 'long': 46.71179, 'violation': 'Major Asphalt', 'details': 'Major Asphalt', 'display_img': '40.jpg', 'violation_time': '14:29', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 5, 'street_name': 'Al Madina Al Munawwarah Rd', 'violation_type_id': 7, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.62667, 'long': 46.71159, 'violation': 'Minor Asphalt', 'details': 'Minor Asphalt', 'display_img': '42.jpg', 'violation_time': '14:29', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 5, 'street_name': 'Al Madina Al Munawwarah Rd', 'violation_type_id': 1, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.62503,46.7092', 'end_latlng': '24.62488,46.70893'}], 'side02': [{'start_latlng': '24.62704,46.71216', 'end_latlng': '24.62667,46.71159'}], 'total_violations': 6, 'ref': '24.62503,46.7092', 'date': ''}, {'street_id': 6, 'street_name': 'King Fahd Rd', 'violation': [{'lat': 24.6475, 'long': 46.70259, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '3.jpg', 'violation_time': '14:13', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67188, 'long': 46.69218, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '5.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67152, 'long': 46.69241, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '7.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67134, 'long': 46.69253, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '9.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.68044, 'long': 46.68813, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '10.jpg', 'violation_time': '14:10', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.66005, 'long': 46.70085, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '10.jpg', 'violation_time': '14:12', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67117, 'long': 46.69265, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '12.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.70544, 'long': 46.67516, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'accurate': 95, 'risk': 2, 'display_img': '13.jpg', 'violation_time': '14:05', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.671, 'long': 46.69278, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'accurate': 95, 'risk': 2, 'display_img': '14.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67083, 'long': 46.69293, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '16.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.65959, 'long': 46.70091, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '17.jpg', 'violation_time': '14:12', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67066, 'long': 46.69307, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'accurate': 95, 'risk': 2, 'display_img': '18.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67032, 'long': 46.69339, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '22.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67032, 'long': 46.69339, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'accurate': 95, 'risk': 2, 'display_img': '23.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67, 'long': 46.69373, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '25.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.66984, 'long': 46.69391, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'accurate': 95, 'risk': 2, 'display_img': '26.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.66968, 'long': 46.69409, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'accurate': 95, 'risk': 2, 'display_img': '28.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.66968, 'long': 46.69409, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'display_img': '30.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.64381, 'long': 46.70303, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '32.jpg', 'violation_time': '14:13', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.70086, 'long': 46.6776, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'display_img': '33.jpg', 'violation_time': '14:06', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.64324, 'long': 46.70308, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '34.jpg', 'violation_time': '14:13', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.64306, 'long': 46.7031, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '35.jpg', 'violation_time': '14:13', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.64289, 'long': 46.70312, 'violation': 'Minor Asphalt', 'details': 'Minor Asphalt', 'display_img': '37.jpg', 'violation_time': '14:13', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 1, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.64273, 'long': 46.70314, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '39.jpg', 'violation_time': '14:13', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.6422, 'long': 46.70319, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '41.jpg', 'violation_time': '14:13', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.70381, 'long': 46.67597, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '43.jpg', 'violation_time': '14:05', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.65328, 'long': 46.70177, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '45.jpg', 'violation_time': '14:12', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.7068, 'long': 46.67471, 'violation': 'Communication Tower', 'details': 'Communication Tower', 'display_img': '49.jpg', 'violation_time': '14:04', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 11, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67365, 'long': 46.69122, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '50.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.6315, 'long': 46.7043, 'violation': 'Street Sweeping', 'details': 'Street Sweeping', 'display_img': '51.jpg', 'violation_time': '14:15', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 9, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.69054, 'long': 46.68283, 'violation': 'Major Asphalt', 'details': 'Major Asphalt', 'display_img': '52.jpg', 'violation_time': '14:09', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 7, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67348, 'long': 46.69132, 'violation': 'Rubble Source', 'details': ' Rubble Source', 'display_img': '55.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.6733, 'long': 46.69141, 'violation': 'Rubble Source', 'details': ' Rubble Source', 'display_img': '56.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.67312, 'long': 46.69151, 'violation': 'Rubble Source', 'details': ' Rubble Source', 'display_img': '57.jpg', 'violation_time': '14:11', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 6, 'street_name': 'King Fahd Rd', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.67365,46.69122', 'end_latlng': '24.66968,46.69409'}, {'start_latlng': '24.66005,46.70085', 'end_latlng': '24.65959,46.70091'}, {'start_latlng': '24.65328,46.70177', 'end_latlng': '24.65288,46.70177'}, {'start_latlng': '24.6475,46.70259', 'end_latlng': '24.647100000000002,46.70259'}, {'start_latlng': '24.64381,46.70303', 'end_latlng': '24.6422,46.70319'}], 'side02': [{'start_latlng': '24.68044,46.68813', 'end_latlng': '0,0'}, {'start_latlng': '24.69054,46.68283', 'end_latlng': '24.690939999999998,46.68263'}, {'start_latlng': '24.70086,46.6776', 'end_latlng': '24.701259999999998,46.6774'}], 'total_violations': 34, 'ref': '24.6475,46.70259', 'date': ''}, {'street_id': 8, 'street_name': 'Al Muqaybirah Street', 'violation': [{'lat': 24.62819, 'long': 46.70886, 'violation': 'Minor Asphalt', 'details': 'Minor Asphalt', 'display_img': '44.jpg', 'violation_time': '14:23', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 8, 'street_name': 'Al Muqaybirah Street', 'violation_type_id': 1, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.62819, 'long': 46.70897, 'violation': 'Minor Asphalt', 'details': ' Minor Asphalt', 'display_img': '58.jpg', 'violation_time': '14:23', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 8, 'street_name': 'Al Muqaybirah Street', 'violation_type_id': 1, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.62819,46.70886', 'end_latlng': '0,0'}], 'side02': [{'start_latlng': '24.62819,46.70897', 'end_latlng': '0,0'}], 'total_violations': 2, 'ref': '24.62819,46.70886', 'date': ''}, {'street_id': 9, 'street_name': 'Al Madinah Al Munawwarah Road', 'violation': [{'lat': 24.62507, 'long': 46.70926, 'violation': 'Rubble Source', 'details': 'Rubble Source', 'display_img': '47.jpg', 'violation_time': '14:19', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 9, 'street_name': 'Al Madinah Al Munawwarah Road', 'violation_type_id': 8, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.62507,46.70926', 'end_latlng': '24.62547,46.70926'}], 'side02': [], 'total_violations': 1, 'ref': '24.62507,46.70926', 'date': ''}, {'street_id': 10, 'street_name': 'King Faisal Road', 'violation': [{'lat': 24.63044, 'long': 46.71588, 'violation': 'Median', 'details': 'Median', 'accurate': 95, 'risk': 2, 'display_img': '15.jpg', 'violation_time': '14:18', 'violation_date': '2022-10-08', 'street_id': 10, 'street_name': 'King Faisal Road', 'violation_type_id': 10, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.63015, 'long': 46.71597, 'violation': 'Median', 'details': 'Median', 'accurate': 95, 'risk': 2, 'display_img': '21.jpg', 'violation_time': '14:18', 'violation_date': '2022-10-08', 'street_id': 10, 'street_name': 'King Faisal Road', 'violation_type_id': 10, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.63044,46.71588', 'end_latlng': '24.63015,46.71597'}], 'side02': [], 'total_violations': 2, 'ref': '24.63044,46.71588', 'date': ''}, {'street_id': 11, 'street_name': 'الداغمة', 'violation': [{'lat': 24.63184, 'long': 46.7158, 'violation': 'Median', 'details': 'Median', 'accurate': 95, 'risk': 2, 'display_img': '27.jpg', 'violation_time': '14:28', 'violation_date': '2022-10-08', 'street_id': 11, 'street_name': 'الداغمة', 'violation_type_id': 10, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.63173, 'long': 46.71584, 'violation': 'Median', 'details': 'Median', 'accurate': 95, 'risk': 2, 'display_img': '29.jpg', 'violation_time': '14:28', 'violation_date': '2022-10-08', 'street_id': 11, 'street_name': 'الداغمة', 'violation_type_id': 10, 'start_latlng': 0, 'end_latlng': 0}, {'lat': 24.63161, 'long': 46.71588, 'violation': 'Median', 'details': 'Median', 'display_img': '31.jpg', 'violation_time': '14:28', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 11, 'street_name': 'الداغمة', 'violation_type_id': 10, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.63184,46.7158', 'end_latlng': '24.63161,46.71588'}], 'side02': [], 'total_violations': 3, 'ref': '24.63184,46.7158', 'date': ''}, {'street_id': 14, 'street_name': 'وادي عتبة', 'violation': [{'lat': 24.63196, 'long': 46.71576, 'violation': 'Median', 'details': 'Median', 'accurate': 95, 'risk': 2, 'display_img': '24.jpg', 'violation_time': '14:28', 'violation_date': '2022-10-08', 'street_id': 14, 'street_name': 'وادي عتبة', 'violation_type_id': 10, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.63196,46.71576', 'end_latlng': '24.63206,46.71616'}], 'side02': [], 'total_violations': 1, 'ref': '24.63196,46.71576', 'date': ''}, {'street_id': 15, 'street_name': 'Al Atayif', 'violation': [{'lat': 24.63024, 'long': 46.70724, 'violation': 'Minor Asphalt', 'details': 'Minor Asphalt', 'display_img': '48.jpg', 'violation_time': '14:25', 'violation_date': '2022-10-08', 'accurate': 95, 'risk': 2, 'street_id': 15, 'street_name': 'Al Atayif', 'violation_type_id': 1, 'start_latlng': 0, 'end_latlng': 0}], 'side01': [{'start_latlng': '24.63024,46.70724', 'end_latlng': '24.63064,46.70724'}], 'side02': [], 'total_violations': 1, 'ref': '24.63024,46.70724', 'date': ''}]
# print(len(l))
# for i in range(len(l)):
#     print(l[i]['street_name'])
#     #'total_violations': 1, 'ref': '24.63024,46.70724', 'date': ''
#     print("\ttotal_violations: "+str(l[i]['total_violations']))
#     print("\tRef: " + str(l[i]['ref']))
#     print("\tSide01:")
#     for j in l[i]['side01']:
#         print("\t\t"+str(j))
#     print("\tSide02:")
#     for j in l[i]['side02']:
#         print("\t\t" + str(j))

import polyline
import requests

url = "https://maps.googleapis.com/maps/api/directions/json?origin=24.681264,46.694644&destination=24.692974,46.721036&key=AIzaSyAhpqm1hIWBkVzKvf7uyqCmYNRxwQwbZzo"

response = requests.request("GET", url, headers={}, data={})
l = polyline.decode(response.json()["routes"][0]['overview_polyline']['points'])
al = []
for i in l:
    temp = {'lat': i[0], 'lng': i[1]}
    al.append(temp)

# l = [1,2,3,4,5]
# h= str(l)
# print(h)
# print(type(h))

# li = [[1,1,1],[2,2,2],[3,3,3]]
# for i in range(len(li)):
#     for j in range(len(li[i])):
#         li[i][j] = li[i][j] * 2
# 
# print(li )
