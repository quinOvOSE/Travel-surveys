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

def LocationID_PROCESS(x,Cite):
    familyid = int(x.split('_')[0])
    memberid = int(x.split('_')[1])
    temp = Cite[(Cite['JiaTingID']==familyid) & (Cite['ChengYuanID']==memberid)]

    return list(range(len(1,temp+1)))

def LocationType_first(x,House_Member):
    if x['LingChen3DianZaiNa']==1:
        return 'Home'
    elif x['LingChen3DianZaiNa']==3:
        return 'Other'
    else:
        if x['ZaiGanShenMe'] == 3:
            return 'Workplace'
        elif x['ZaiGanShenMe'] == 5:
            return 'School'
        else:
            temp = House_Member[(House_Member['JiaTingID']==x['JiaTingID'])&(House_Member['ChengYuanID']==x['ChengYuanID'])]['RenYuanLeiBie']
            temp = list(temp)[0]
            if temp in [1.0,2.0]:
                return 'Workplace'
            elif temp in [3.0,4.0,5.0]:
                return 'School'
            else:
                return 'Other'

def _LocationType_others(x,House_Member):
    if x['JiXuHuanChengQingKuang'] == 2:
        return 'Transfer'
    else:
        if x['DaoDaDiDian']==1:
            return 'Home'
        elif x['DaoDaDiDian'] ==3:
            return 'Other'
        elif x['DaoDaDiDian'] == 2:
            if x['ZaiNaGanShenMe']==3:
                return 'Workplace'
            elif x['ZaiNaGanShenMe']==5:
                return 'School'
            else:
                temp = House_Member[(House_Member['JiaTingID']==x['JiaTingID'])&(House_Member['ChengYuanID']==x['ChengYuanID'])]['RenYuanLeiBie']
                temp = list(temp)[0]
                if temp in [1.0,2.0]:
                    return 'Workplace'
                elif temp in [3.0,4.0,5.0]:
                    return 'School'
                else:
                    return 'Other'
        else:
            print('error occur in _LocationType_others')


def LocationType_others(x,Cite,House_Member):
    familyid = int(x.split('_')[0])
    memberid = int(x.split('_')[1])
    person_cite = Cite[(Cite['JiaTingID']==familyid)&(Cite['ChengYuanID']==memberid)]
    #print(person_cite)
    person_cite_ = pd.DataFrame.copy(person_cite,deep=True)
    person_cite_['list'] = person_cite_.apply(_LocationType_others,args=(House_Member,),axis=1)
    return list(person_cite_['list'])

def LocationAddress_first(x,House,House_Member):
    if x['LingChen3DianZaiNa']==1:
        return [list(House[House['JiaTingID']==x['JiaTingID']]['DiZhi'])[0]]
    elif x['LingChen3DianZaiNa']==3:
        return [list(x['QiTaDiFangDiZhi'])[0]]
    elif x['LingChen3DianZaiNa']==2:
        temp = House_Member[(House_Member['JiaTingID']==x['JiaTingID'])&(House_Member['ChengYuanID']==x['ChengYuanID'])]['XiangXiDizhi']
        return [list(temp)[0]]
    else:
        print('error occur in LocationAddress_first')

def _LocationAddress_others(x,Cite,House_Member,House):
    if x['JiXuHuanChengQingKuang'] == 2:
        return list(x['HuanChengDiDian'])[0]
    else:
        if x['DaoDaDiDian']==1:
            home = list(House[House['JiaTingID']==x['JiaTingID']]['DiZhi'])[0]
            return home
        elif x['DaoDaDiDian'] ==2:
            work = House_Member[(House_Member['JiaTingID']==x['JiaTingID'])&(House_Member['ChengYuanID']==x['ChengYuanID'])]['XiangXiDizhi']
            return list(work)[0]
        elif x['DaoDaDiDian'] ==3:
            return x['DaoDaDiDianQT']
        else:
            print('error occor in _LocationAddress_others')

def LocationAddress_others(x,Cite,House_Member,House):
    familyid = int(x.split('_')[0])
    memberid = int(x.split('_')[1])
    person_cite = Cite[(Cite['JiaTingID']==familyid)&(Cite['ChengYuanID']==memberid)]
    #print(person_cite)
    person_cite_ = pd.DataFrame.copy(person_cite,deep=True)
    person_cite_['list'] = person_cite_.apply(_LocationAddress_others,args=(Cite,House_Member,House,),axis=1)
    return list(person_cite_['list'])

def LocationTAZ_first(x,House,House_Member):
    if x['LingChen3DianZaiNa']==1:
        return [list(House[House['JiaTingID']==x['JiaTingID']]['XiaoQuBianHao'])[0]]
    elif x['LingChen3DianZaiNa']==2:
        temp = House_Member[(House_Member['JiaTingID']==x['JiaTingID'])&(House_Member['ChengYuanID']==x['ChengYuanID'])]['XiaoQuDaiMa']
        return [list(temp)[0]]
    elif x['LingChen3DianZaiNa']==3:
        return [x['QiTaDiFangXiaoQuhao']]
    else:
        print('error occur in LocationTAZ_first')


def _LocationTAZ_others(x,Cite,House_Member,House):
    if x['JiXuHuanChengQingKuang'] == 2:
        return 'null'
    else:
        if x['DaoDaDiDian']==1:
            home = list(House[House['JiaTingID']==x['JiaTingID']]['XiaoQuBianHao'])[0]
            return home
        elif x['DaoDaDiDian'] ==2:
            work = House_Member[(House_Member['JiaTingID']==x['JiaTingID'])&(House_Member['ChengYuanID']==x['ChengYuanID'])]['XiaoQuDaiMa']
            return list(work)[0]
        elif x['DaoDaDiDian'] ==3:
            return x['DaoDaDiDianXiaoQuHao']
        else:
            print('error occor in _LocationAddress_others')

def LocationTAZ_others(x,Cite,House_Member,House):
    familyid = int(x.split('_')[0])
    memberid = int(x.split('_')[1])
    person_cite = Cite[(Cite['JiaTingID']==familyid)&(Cite['ChengYuanID']==memberid)]
    #print(person_cite)
    person_cite_ = pd.DataFrame.copy(person_cite,deep=True)
    person_cite_['list'] = person_cite_.apply(_LocationTAZ_others,args=(Cite,House_Member,House,),axis=1)
    return list(person_cite_['list'])

def ActInLocation_first(x,Likai_person):
    familyid = int(x.split('_')[0])
    memberid = int(x.split('_')[1])
    output = Likai_person[(Likai_person['JiaTingID']==familyid)&(Likai_person['ChengYuanID']==memberid)]
    if pd.isnull(list(output['ZaiGanShenMe'])[0]):
        return [1.0]
    else:
        return [list(output['ZaiGanShenMe'])[0]]


def _ActInLocation_others(x):
    if pd.isnull(x['ZaiNaGanShenMe']):
        if pd.isnull(x['DaoDaDiDian']):
            return 15
        elif x['DaoDaDiDian']==1:
            return 16
        else:
            print('error occur in _ActInLocation_others')
    else:
        output = x['ZaiNaGanShenMe']
        if output>16:
            output_ = list(str(output))
            output__ = '-'.join(list(map(lambda x,y:x+y,output_[::2],output_[1::2])))
            return output__
        else:
            return output

def ActInLocation_others(x,Cite):
    familyid = int(x.split('_')[0])
    memberid = int(x.split('_')[1])
    person_cite = Cite[(Cite['JiaTingID']==familyid)&(Cite['ChengYuanID']==memberid)]
    person_cite_ = pd.DataFrame.copy(person_cite,deep=True)
    person_cite_['list'] = person_cite_.apply(_ActInLocation_others,axis=1)
    return list(person_cite_['list'])

# INPUT
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

district_dict = {1:'西城区',2:'东城区',3:'东城区',4:'西城区',5:'海淀区',
6:'朝阳区',7:'丰台区',8:'石景山区',9:'昌平区',10:'顺义区',11:'通州区',
12:'大兴区',13:'房山区',14:'门头沟区',15:'延庆区',16:'怀柔区',17:'密云区',18:'平谷区'}

# DATA CLEAN with function of DATA_CLEAN
Cite,Travel,Vehicle,License_Plate,House_Member,House = DATA_CLEAN(Table_Cite,Table_Travel,Table_Vehicle,Table_License_Plate,Table_House_Member,Table_House)


#print(Travel[:10])
# filter person who generate a travel
Travel['Filter'] = Travel.apply(lambda x:1 if x['LiKaiQingKuang']==1 and (pd.isnull(x['QiTaDiFangXiaoQuhao']) or (x['QiTaDiFangXiaoQuhao'] >=10000 and x['QiTaDiFangXiaoQuhao'] <=200000)) else 0,axis=1)
Likai_person = list(Travel.groupby("Filter"))[1][1]

Travel_person = pd.DataFrame()

Travel_person['FamilyID'] = Likai_person['JiaTingID']

Travel_person['PersonID'] = Likai_person['JiaTingID'].apply(str)+'_'+Likai_person['ChengYuanID'].apply(str)

Travel_person['LocationID'] = Travel_person['PersonID'].apply(LocationID_PROCESS,args=(Cite,))

Travel_person['LocationType'] = Likai_person.apply(LocationType_first,args=(House_Member,),axis=1)+Travel_person['PersonID'].apply(LocationType_others,args=(Cite,House_Member))
Travel_person['LocationAddress'] = Likai_person.apply(LocationAddress_first,args=(House,House_Member,),axis=1)+Travel_person['PersonID'].apply(LocationAddress_others,args=(Cite,House_Member,House,))
Travel_person['LocationTAZ']  = Likai_person.apply(LocationTAZ_first,args=(House,House_Member,),axis=1)+Travel_person['PersonID'].apply(LocationTAZ_others,args=(Cite,House_Member,House,))

Travel_person['ActInLocation'] = Travel_person['PersonID'].apply(ActInLocation_first,args=(Likai_person,))+Travel_person['PersonID'].apply(ActInLocation_others,args=(Cite,))
