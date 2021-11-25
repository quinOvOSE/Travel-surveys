#!/usr/bin/python
# -*- coding:utf-8 -*-

# 导入需要的库
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
import os
from Data_clean_process import DATA_CLEAN
import datetime

tqdm.pandas(desc='pandas bar')
pd.set_option('precision', 14)
def format_time(a):
    lst = a.split('|')
    return  datetime.datetime(int(lst[0]),
                              int(lst[1]),
                              int(lst[2]),
                              int(lst[3]),
                              int(lst[4]),
                              int(lst[5]))

def time_distance(a,b):
    time_a = format_time(a)
    time_b = format_time(b)
    return (time_b-time_a).seconds

def Search_on_DataFrame(x,df):
    if type(x) == str:
        familyid = int(x.split('_')[0])
        memberid = int(x.split('_')[1])
        temp = df[(df['JiaTingID']==familyid) & (df['ChengYuanID']==memberid)]
        return temp
    elif type(x) == int:
        temp = df[df['JiaTingID']==x]
        return temp

def LocationID_PROCESS(x,Cite):
    #print(x)
    familyid = int(x.split('_')[0])
    memberid = int(x.split('_')[1])
    temp = Cite[(Cite['JiaTingID']==familyid) & (Cite['ChengYuanID']==memberid)]
    #print(len(temp))
    return list(range(len(temp)+1))

def LocationType_first(x,Likai_person,House_Member):
    df_filter = Search_on_DataFrame(x,Likai_person)
    if df_filter['LingChen3DianZaiNa'].__int__()==1:
        return ['Home']
    elif df_filter['LingChen3DianZaiNa'].__int__()==3:
        return ['Other']
    else:
        if df_filter['ZaiGanShenMe'].__int__() == 3:
            return ['Workplace']
        elif df_filter['ZaiGanShenMe'].__int__() == 5:
            return ['School']
        else:
            print(x)
            temp = House_Member[
                (House_Member['JiaTingID']==df_filter['JiaTingID'].__int__())&(House_Member['ChengYuanID']==df_filter['ChengYuanID'].__int__())
                 ]['RenYuanLeiBie']
            temp = list(temp)[0]
            if temp in [1.0,2.0]:
                return ['Workplace']
            elif temp in [3.0,4.0,5.0]:
                return ['School']
            else:
                return ['Other']

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
                #print(temp)
                if temp in [1.0,2.0]:
                    return 'Workplace'
                elif temp in [3.0,4.0,5.0]:
                    return 'School'
                else:
                    return 'Other'
        else:
            print('error occur in _LocationType_others')
def LocationType_others(x,Cite,House_Member):
    df_filter = Search_on_DataFrame(x,Cite).sort_values(by='DiDianID')
    person_cite_ = pd.DataFrame.copy(df_filter,deep=True)
    person_cite_['list'] = person_cite_.apply(_LocationType_others,args=(House_Member,),axis=1)
    return list(person_cite_['list'])

def LocationAddress_first(x,Likai_person,House,House_Member):
    df_filter = Search_on_DataFrame(x,Likai_person)
    if df_filter['LingChen3DianZaiNa'].__int__()==1:
        return [House[House['JiaTingID'] == df_filter['JiaTingID'].__int__()]['DiZhi'].any()]
    elif df_filter['LingChen3DianZaiNa'].__int__()==3:
        return [df_filter['QiTaDiFangDiZhi'].any()]
    elif df_filter['LingChen3DianZaiNa'].__int__()==2:
        temp = House_Member[(House_Member['JiaTingID']==df_filter['JiaTingID'])&(House_Member['ChengYuanID']==df_filter['ChengYuanID'])]['XiangXiDizhi']
        return [temp.any()]
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
    df_filter = Search_on_DataFrame(x,Cite).sort_values(by='DiDianID')
    person_cite_ = pd.DataFrame.copy(df_filter,deep=True)
    person_cite_['list'] = person_cite_.apply(_LocationAddress_others,args=(Cite,House_Member,House,),axis=1)
    return list(person_cite_['list'])

def LocationTAZ_first(x,Likai_person,House,House_Member):
    df_filter = Search_on_DataFrame(x,Likai_person)
    if df_filter['LingChen3DianZaiNa'].__int__()==1:
        return [House[House['JiaTingID']==df_filter['JiaTingID'].__int__()]['XiaoQuBianHao'].__int__()]
    elif df_filter['LingChen3DianZaiNa'].__int__()==2:
        temp = House_Member[(House_Member['JiaTingID']==df_filter['JiaTingID'])&(House_Member['ChengYuanID']==df_filter['ChengYuanID'])]['XiaoQuDaiMa']
        return [temp.__int__()]
    elif df_filter['LingChen3DianZaiNa'].__int__()==3:
        return [df_filter['QiTaDiFangXiaoQuhao'].__int__()]
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
    df_filter = Search_on_DataFrame(x,Cite).sort_values(by='DiDianID')

    #print(person_cite)
    person_cite_ = pd.DataFrame.copy(df_filter,deep=True)
    person_cite_['list'] = person_cite_.apply(_LocationTAZ_others,args=(Cite,House_Member,House,),axis=1)
    return list(person_cite_['list'])



def ActInLocation_first(x,Likai_person):
    df_filter = Search_on_DataFrame(x,Likai_person)
    if pd.isnull(list(df_filter['ZaiGanShenMe'])[0]):
        return [1.0]
    else:
        return [list(df_filter['ZaiGanShenMe'])[0]]


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
    df_filter = Search_on_DataFrame(x,Cite).sort_values(by='DiDianID')
    person_cite_ = pd.DataFrame.copy(df_filter,deep=True)
    person_cite_['list'] = person_cite_.apply(_ActInLocation_others,axis=1)
    return list(person_cite_['list'])


def _ArriveLocTime_PROCESS(x):
    if x['JiaoTongFangShi']==1:
        return x['BuXingDaoDaSJ']
    elif x['JiXuHuanChengQingKuang']==2:
        return x['XiaCheDaoDaSJ']
    else:
        time = x['XiaCheDaoDaSJ']

        dt = datetime.datetime(1990,1,1,time.hour,time.minute)
        dt = dt+datetime.timedelta(minutes=x['BuHuanChengZouLuSJ'])
        return dt

def ArriveLocTime_PROCESS(x,Likai_person,Cite):
    df_filter = Search_on_DataFrame(x,Likai_person)
    #get year month and day
    date = list(df_filter['ChuXinRQ'])[0]
    year = str(date.year)
    month =  str(date.month)
    day =  str(date.day)
    #get time
    df_filter = Search_on_DataFrame(x,Cite).sort_values(by='DiDianID')
    times = df_filter.apply(_ArriveLocTime_PROCESS,axis=1)
    output = []
    for i in times:
        output.append('|'.join([year,month,day,str(i.hour),str(i.minute),str(i.second)]))

    return ['null']+output


def LeaveLocTime_first(x,Likai_person,Cite):
    df_filter = Search_on_DataFrame(x,Likai_person)
    #get year month and day
    date = list(df_filter['ChuXinRQ'])[0]
    year = str(date.year)
    month =  str(date.month)
    day =  str(date.day)
    #get time
    time = df_filter['LiKaiSJ'].any()
    output = '|'.join([year,month,day,str(time.hour),str(time.minute),str(time.second)])
    return [output]

def LeaveLocTime_others(x,Likai_person,Cite):
    df_filter = Search_on_DataFrame(x,Likai_person)
    #get year month and day
    date = list(df_filter['ChuXinRQ'])[0]
    year = str(date.year)
    month =  str(date.month)
    day =  str(date.day)
    #get time
    df_filter = Search_on_DataFrame(x,Cite).sort_values(by='DiDianID')
    times = df_filter.apply(lambda x:
                            x['XiaCheDaoDaSJ'] if x['JiXuHuanChengQingKuang']==2 else x['LiKaiSJ'] if x['LiKaiQingKuang']!=2 else -1
                            ,axis=1)
    output = []
    for i in times:
        if i != -1:
            output.append('|'.join([year,month,day,str(i.hour),str(i.minute),str(i.second)]))
        else:
            output.append(-1)
    return output

def StayDuration_PROCESS(x):
    #print(x)
    end = x['ArriveLocTime']
    start = x['LeaveLocTime']

    start = start[:-1]
    end = end[1:]
    return [-1]+list(map(lambda i,j:time_distance(i,j),start,end))+[-1]

def ModeToAccessLoc_PROCESS(x,Cite):
    df_filter = Search_on_DataFrame(x,Cite).sort_values(by='DiDianID')
    fangshi = list(df_filter['JiaoTongFangShi'])
    return [-1]+fangshi


# INPUT
Table_Cite_path = '../data/家庭成员出行地点表.xlsx'
Table_Travel_path = '../data/家庭成员出行表.xlsx'
Table_Vehicle_path = '../data/家庭成员拥有机动车情况表.csv'
Table_License_Plate_path = '../data/家庭成员汽车摇号表.csv'
Table_House_Member_path = '../data/家庭成员表.csv'
Table_House_path = '../data/家庭背景资料表.csv'

Table_Cite = pd.read_excel(Table_Cite_path)
Table_Travel = pd.read_excel(Table_Travel_path)

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

print('Build FamilyID ... ')
Travel_person['FamilyID'] = Likai_person['JiaTingID']
print('DONE')

print('Build PersonID ... ')
Travel_person['PersonID'] = Likai_person['JiaTingID'].progress_apply(str)+'_'+Likai_person['ChengYuanID'].progress_apply(str)
print('DONE')

print('Build LocationID ... ')
#Travel_person['LocationID'] = Travel_person['PersonID'].progress_apply(LocationID_PROCESS,args=(Cite,))
print('DONE')

print('Build LocationType ... ')
#Travel_person['LocationType'] = Travel_person['PersonID'].progress_apply(LocationType_first,args=(Likai_person,House_Member,))+Travel_person['PersonID'].progress_apply(LocationType_others,args=(Cite,House_Member))
print('DONE')

print('Build LocationAddress... ')
#Travel_person['LocationAddress'] =  Travel_person['PersonID'].progress_apply(LocationAddress_first,args=(Likai_person,House,House_Member,))+Travel_person['PersonID'].progress_apply(LocationAddress_others,args=(Cite,House_Member,House,))
print('DONE')

print('Build LocationTAZ ... ')
#Travel_person['LocationTAZ'] = Travel_person['PersonID'].progress_apply(LocationTAZ_first,args=(Likai_person,House,House_Member,))+Travel_person['PersonID'].progress_apply(LocationTAZ_others,args=(Cite,House_Member,House,))
print('DONE')

print('Build ActInlocation ... ')
#Travel_person['ActInLocation'] = Travel_person['PersonID'].progress_apply(ActInLocation_first,args=(Likai_person,))+Travel_person['PersonID'].progress_apply(ActInLocation_others,args=(Cite,))
print('DONE')

print('Build ArriveLoctime ... ')
Travel_person['ArriveLocTime']  = Travel_person['PersonID'].progress_apply(ArriveLocTime_PROCESS,args=(Likai_person,Cite))
print('DONE')

print('Build Leaveloctime ... ')
Travel_person['LeaveLocTime'] = Travel_person['PersonID'].progress_apply(LeaveLocTime_first,args=(Likai_person,Cite))+Travel_person['PersonID'].progress_apply(LeaveLocTime_others,args=(Likai_person,Cite))
print('DONE')

print('Build StayDuration ... ')
Travel_person['StayDuration'] = Travel_person.progress_apply(StayDuration_PROCESS,axis=1)
print('DONE')

print('Build ModeToAccessLoc ... ')
Travel_person['ModeToAccessLoc'] = Travel_person['PersonID'].progress_apply(ModeToAccessLoc_PROCESS,args=(Cite,))
print('DONE')
