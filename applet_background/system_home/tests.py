import datetime
import random
import re

# Create your tests here.
# old_day = (date.today() - timedelta(seconds=7)).strftime("%Y-%m-%d 00:00:00")
# now_day = date.today().strftime("%Y-%m-%d %H:%M:%S")
# print(old_day)
# print(now_day)

# from applet_background.link_config import con_mysql

# print(datetime.now() - timedelta(days=7))
# print(datetime.now())

# con_mysql_connect = con_mysql.connection()
# cursor = con_mysql_connect.cursor()
# cursor.execute('SELECT agentName FROM agent_list')
# data = cursor.fetchall()
# cursor.close()
# con_mysql_connect.close()
# agentList = [i[0] for i in data]
# print(agentList)

# from geopy.geocoders import Nominatim
#
# geolocator = Nominatim()
# location = geolocator.geocode('宝安区')
# print(location.address)
import string
import time

# from applet_background.link_config import con_mysql
from system_home.func_for_system_views import address_location

"""
将查询地理定位到地址和坐标
"""

# from geopy.geocoders import Baidu

# for i in ["宝安区", '金牛区', '南山区', '深圳市桥头镇']:
#     location = geolocator.geocode(i)
#     print(location)
#     print((location.latitude, location.longitude))


# def address_location(address):
#     location = geolocator.geocode(address)
#     return {'latitude': location.latitude, 'longitude': location.longitude}
#
#
# location = geolocator.geocode('宝安区')
# print(location.latitude, location.longitude)

# print(address_location('宝安区'))

#
# con_mysql_connect = con_mysql.connection()
# cursor = con_mysql_connect.cursor()
# cursor.execute("SELECT deviceId, city FROM hos_list ORDER BY city")
# data = cursor.fetchall()
# cursor.close()
# con_mysql_connect.close()
# dict_city_device = dict()
# for i in data:
#     if i[1] in dict_city_device.keys():
#         dict_city_device[i[1]].append(i[0])
#     else:
#         dict_city_device[i[1]] = [i[0]]
# print(dict_city_device)

# print(time.time())
# print(str(time.time())[2:13].replace('.', random.choice(string.ascii_letters)))

# sql_1 = "SELECT COUNT(1), COUNT(DISTINCT hosName), city FROM hos_list GROUP BY city"
# sql_2 = "SELECT COUNT(1), city FROM order_list AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
#         " GROUP BY d.`city`"
# sql_3 = "SELECT COUNT(1), city FROM maintain_repair AS o, hos_list AS d WHERE o.`deviceId` = d.`deviceId`" \
#         " GROUP BY  d.`city`"

#
# def table_data_by_sql(sql_1, sql_2, sql_3):
#     con_mysql_connect = con_mysql.connection()
#     cursor = con_mysql_connect.cursor()
#     cursor.execute(sql_1)
#     data_1 = cursor.fetchall()
#     cursor.execute(sql_2)
#     data_2 = cursor.fetchall()
#     cursor.execute(sql_3)
#     data_3 = cursor.fetchall()
#     cursor.close()
#     con_mysql_connect.close()
#     return_dict = dict()
#     for d1 in data_1:
#         return_dict[d1[2]] = {
#             'deviceNum': d1[0] if d1[0] is not None else 0,
#             'hosNum': d1[1] if d1[1] is not None else 0,
#             'orderNum': 0,
#             'repairs': 0,
#         }
#     for d2 in data_2:
#         if d2[1] in return_dict.keys():
#             return_dict[d2[1]]['orderNum'] = d2[0] if d2[0] is not None else 0
#         else:
#             return_dict[d2[1]] = {
#                 'deviceNum': 0,
#                 'hosNum': 0,
#                 'orderNum': d2[0] if d2[0] is not None else 0,
#                 'repairs': 0,
#             }
#     for d3 in data_3:
#         if d3[1] in return_dict.keys():
#             return_dict[d3[1]]['repairs'] = d3[0] if d3[0] is not None else 0
#         else:
#             return_dict[d3[1]] = {
#                 'deviceNum': 0,
#                 'hosNum': 0,
#                 'orderNum': 0,
#                 'repairs': d3[0] if d3[0] is not None else 0,
#             }
#     return return_dict
#
#
# def map_data(sql_1, sql_2, sql_3):
#     '''
#
#     :param data_1: 查询结果
#     :param data_2: 同上
#     :param data_3: 同上
#     :return:
#     '''
#     con_mysql_connect = con_mysql.connection()
#     cursor = con_mysql_connect.cursor()
#     cursor.execute(sql_1)
#     data_1 = cursor.fetchall()
#     cursor.execute(sql_2)
#     data_2 = cursor.fetchall()
#     cursor.execute(sql_3)
#     data_3 = cursor.fetchall()
#     cursor.close()
#     con_mysql_connect.close()
#     dict_data = dict()
#     for data in data_1:
#         dict_data[data[2] + data[3]] = {'useCount': 0 if data[0] is None else data[0],
#                                         'totalIncome': 0 if data[1] is None else data[1],
#                                         'deviceNum': 0, 'hosNum': 0, 'repairsCount': 0}
#     for d2 in data_2:
#         if d2[2] + d2[3] in dict_data.keys():
#             dict_data[d2[2] + d2[3]]['deviceNum'] = 0 if d2[0] is None else d2[0]
#             dict_data[d2[2] + d2[3]]['hosNum'] = 0 if d2[1] is None else d2[1]
#         else:
#             dict_data[d2[2] + d2[3]] = {'useCount': 0, 'totalIncome': 0,
#                                         'deviceNum': 0 if d2[0] is None else d2[0],
#                                         'hosNum': 0 if d2[1] is None else d2[1],
#                                         'repairsCount': 0}
#     for d3 in data_3:
#         if d3[1] + d3[2] in dict_data.keys():
#             location_data = address_location(address=d3[1] + d3[2])
#             dict_data[d3[1] + d3[2]]['deviceNum'] = 0 if d3[0] is None else d3[0]
#             dict_data[d3[1] + d3[2]]['latitude'] = location_data.get('latitude')
#             dict_data[d3[1] + d3[2]]['longitude'] = location_data.get('longitude')
#         else:
#             location_data = address_location(address=d3[1] + d3[2])
#             dict_data[d3[1] + d3[2]] = {'useCount': 0, 'totalIncome': 0,
#                                         'deviceNum': 0,
#                                         'hosNum': 0,
#                                         'repairsCount': 0 if d3[0] is None else d3[0],
#                                         'latitude': location_data.get('latitude'),
#                                         'longitude': location_data.get('longitude')}
#     return dict_data
#
#
# sql_1 = "SELECT COUNT(1),SUM(cost), COUNT(DISTINCT hosName), COUNT(DISTINCT userId)," \
#         " SUBSTRING(o.`startTime`, 1, 7) FROM order_list AS o, hos_list AS d" \
#         " WHERE o.`deviceId` = d.`deviceId` GROUP BY SUBSTRING(o.`startTime`, 1, 7)"
#
# sql_2 = "SELECT COUNT(1),SUBSTRING(importTime, 1, 7) FROM maintain_repair " \
#         "GROUP BY SUBSTRING(importTime, 1, 7)"


# def func_for_get_search(sql_1, sql_2):
#     con_mysql_connect = con_mysql.connection()
#     cursor = con_mysql_connect.cursor()
#     cursor.execute(sql_1)
#     data_1 = cursor.fetchall()
#     cursor.execute(sql_2)
#     data_2 = cursor.fetchall()
#     cursor.close()
#     con_mysql_connect.close()
#     print(data_1)
#     print(data_2)
#     return_dict = dict()
#     for d1 in data_1:
#         return_dict[d1[4]] = {
#             'orderNum': d1[0] if d1[0] is not None else 0,
#             'allIncome': d1[1] if d1[1] is not None else 0,
#             'hosNum': d1[2] if d1[2] is not None else 0,
#             'userNum': d1[3] if d1[3] is not None else 0,
#             'repair': 0,
#         }
#     for d2 in data_2:
#         if d2[1] in return_dict.keys():
#             return_dict[d2[1]]['repair'] = d2[0] if d2[0] is not None else 0
#         else:
#             return_dict[d2[1]] = {
#                 'orderNum': 0,
#                 'allIncome': 0,
#                 'hosNum': 0,
#                 'userNum': 0,
#                 'repair': d2[0] if d2[0] is not None else 0,
#             }
#     return return_dict
