#!/usr/bin/python
# -*- coding:utf-8 -*-

# 导入需要的库
import pandas as pd
import numpy as np
from pprint import pprint
import geopandas as gpd
import tqdm
import json
import os
from shapely.geometry import Point
from geopy.geocoders import Baidu
from geopy.distance import geodesic
from Data_clean_process import DATA_CLEAN

pd.set_option('precision', 14)
def LOCATE_CHECK(p,code,map_data):
    if p == [-1.0,-1.0]:
        return [-1,-1,-1]
    if int(code) == 999999:
        return [-1,-1,-1]

    p_ = Point(p[0],p[1])
    if True in list(map_data.contains(p_)):
        decode_code = list(map_data[map_data.contains(p_)==True]['NO'])[0]
        if decode_code != code:
            A = p[::-1]
            B = [
                list(map_data[map_data['NO']==code]['geometry'])[0].centroid.y,
               list(map_data[map_data['NO']==code]['geometry'])[0].centroid.x
            ]
            dis_ = geodesic(A, B).kilometers
            return([decode_code,code,dis_])
        else:
            return([decode_code,code,0])

    else:
        return([-1,-1,-1])

'''
# 输入
Table_Cite_path = '../data/家庭成员出行地点表.csv'
Table_Travel_path = '../data/家庭成员出行表.csv'
Table_Vehicle_path = '../data/家庭成员拥有机动车情况表.csv'
Table_License_Plate_path = '../data/家庭成员汽车摇号表.csv'
Table_House_Member_path = '../data/家庭成员表.csv'
Table_House_path = '../data/家庭背景资料表.csv'

Table_Cite = pd.read_csv(Table_Cite_path, low_memory=False)
Table_Travel = pd.read_csv(Table_Travel_path, low_memory=False)
Table_Vehicle = pd.read_csv(Table_Vehicle_path, low_memory=False)
Table_License_Plate = pd.read_csv(Table_License_Plate_path, low_memory=False)
Table_House_Member = pd.read_csv(Table_House_Member_path, low_memory=False)
Table_House = pd.read_csv(Table_House_path, low_memory=False)

Set_of_csv = [Table_Cite,
              Table_Travel,
              Table_Vehicle,
              Table_License_Plate,
              Table_House_Member,
              Table_House]
Set_of_name = ['家庭成员出行地点表',
              '家庭成员出行表',
              '家庭成员拥有机动车情况表',
              '家庭成员汽车摇号表',
              '家庭成员表',
              '家庭背景资料表']

travel_purpose_string = {1:'睡觉',2:'吃饭',3:'工作',4:'公务外出',
                         5:'上课或学习',6:'个人事务(银行或就医等)',
                         7:'公务或照顾人',8:'休闲娱乐健身',9:'购物',
                         10:'探亲访友',11:'接送人',12:'陪同他人',
                         13:'取送货物',14:'其他',15:'换乘',16:'回家'}

travel_mode_string = {1:'步行',21:'小客车(私人)',22:'小客车(单位)',
                      23:'小客车(租赁)',3:'客货两用车',4:'货车',
                      5:'摩托车',6:'地铁或城铁',7:'公交车',
                      8:'出租车',9:'单位班车',10:'校车',
                      11:'黑车或摩的',12:'租赁自行车',13:'自行车',
                      14:'电动自行车',15:'其他'}


Cite,Travel,Vehicle,License_Plate,House_Member,House = DATA_CLEAN(Table_Cite,Table_Travel,Table_Vehicle,Table_License_Plate,Table_House_Member,Table_House)

# read map data
Map_path = '../data/2006zones/2006_zones_zone_WGS84_经纬度.shp'
Map_data = gpd.read_file(Map_path)

# read wgs84 lat and long
Locate_file_list = {'Locate_of_家庭成员出行地点表_84.csv':'DaoDaDiDianXiaoQuHao','Locate_of_家庭成员出行表_84.csv':'QiTaDiFangXiaoQuhao','Locate_of_家庭成员表_84.csv':'XiaoQuDaiMa'}
#Locate_name = 'Locate_of_家庭成员出行地点表_84.csv'
Locate_name = 'Locate_of_家庭成员表_84.csv'


Locate_path = os.path.join('../data/',Locate_name)

data = pd.read_csv(Locate_path, low_memory=False)


# set map_code
if Locate_name == 'Locate_of_家庭成员出行地点表_84.csv':
    Map_code = list(Cite[Locate_file_list[Locate_name]])
elif Locate_name == 'Locate_of_家庭成员出行表_84.csv':
    Map_code = list(Travel[Locate_file_list[Locate_name]])
elif Locate_name == 'Locate_of_家庭成员表_84.csv':
    Map_code = list(House_Member[Locate_file_list[Locate_name]])

# set_save_path

Save_name = Locate_name.split('.')[0]+'_output.csv'
Save_path = os.path.join('../data/',Save_name)


# main

lng = list(data['lon84'])
lat = list(data['lat84'])
points = list(map(lambda x,y:[x,y],lng,lat))



output = []
for i in tqdm.tqdm(range(len(data))):
#for i in tqdm.tqdm(range(10)):
    try:
        p = points[i]
        code = Map_code[i]
        aa = LOCATE_CHECK(p,code,Map_data)
        aa.insert(0,i)
        output.append(aa)
    except:
        print(i)

pd.DataFrame(output,columns= ['id','predict_code','real_code','distance']).to_csv(Save_path,index=None)
'''
