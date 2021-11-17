import pandas as pd
import numpy as np
import os
from Data_clean_process import ADDRESS_CLEAN, DATA_CLEAN
from GEOCODERS import GEOCODERS
from LOCATE_CHECK import LOCATE_CHECK
#from multiprocesspandas import applyparallel
import time
import geopandas as gpd
def _ADDRESS_CLEAN(address,district_dict):
    if pd.isnull(address) ==True:
        return '无地址'
    if address in ['※※', '※※※']:
        return '无地址'
    else:
        output =  ADDRESS_CLEAN(address,district_dict)
        return output

def _TAZ_CHECK(df,static_data):
    p = [df['WorkplaceOrSchoolLon'],df['WorkplaceOrSchoolLat']]
    code = df['WorkplaceOrSchoolTAZ']
    output = LOCATE_CHECK(p,code,static_data[0])
    return output
def _TAZ_CHECK1(lon,lat,code):
    map_path = '../data/2006zones/2006_zones_zone_WGS84_经纬度.shp'
    map_data = gpd.read_file(Map_path)

    p = [lon,lat]
    code = code
    output = LOCATE_CHECK(p,code,map_data)
    return output


def XIAOQU_DECODE(code,district_dict):
    if pd.isnull(code) ==False:
        if int(code) == 999999:
            return '京外'
        if len(str(int(code))) == 5:
            return '北京市'+district_dict[int(str(int(code))[0])]

        elif len(str(int(code))) == 6:
            return '北京市'+district_dict[int(str(int(code))[:2])]

        else:
            print(code)
            print('something wrong in XIAOQU_DECODE')
            return '京外'
    else:
        return '无地址'

def RenYuanLeiBie_PROCESS(num):
    num_string = list(str(num))
    if len(num_string) == 1:
        return num
    else:
        if '1' in num_string:
            return 1
        elif '3' in num_string:
            return 3
        elif '2' in num_string:
            return 2
        elif '4' in num_string:
            return 4
        else:
            return int(num_string[0])

def WorkplaceOrSchoolLat_PROCESS(raw_data):
    if type(raw_data) == dict:
        return raw_data['location']['lat']
    else:
        return -1

def WorkplaceOrSchoolLon_PROCESS(raw_data):
    if type(raw_data) == dict:
        return raw_data['location']['lng']
    else:
        return -1


def WorkerOrNot_PROCESS(num):
    if num ==1 or num ==2:
        return 1
    else:
        return 0

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

# SAVE settings
Save_dir = '../documents/'
Save_name ='OutputFiles-PersonLevel.txt'
Save_path = os.path.join(Save_dir,Save_name)

Map_path = '../data/2006zones/2006_zones_zone_WGS84_经纬度.shp'
Map_data = gpd.read_file(Map_path)


Test=False
Decode=False
Address_check=False
if Test:
    print("test 2000 samples!!")
    House_Member = House_Member[:2000]
    print(len(House_Member))



Start_time = time.time()
Person=pd.DataFrame()
Person['FamilyID'] = House_Member['JiaTingID']
Person['PersonID'] = House_Member['JiaTingID'].apply(str)+'_'+House_Member['ChengYuanID'].apply(str)
Person['_MaleOrNot'] = House_Member['XingBie']
Person.loc[Person['_MaleOrNot']==1,'MaleOrNot'] = 1
Person.loc[Person['_MaleOrNot']==2,'MaleOrNot'] = 0
Person['MaleOrNot'] = Person['MaleOrNot'].astype('int')
del Person['_MaleOrNot']
Person['BirthYear'] = House_Member['ChuShengNianFen']
Person['Age'] = 2014-House_Member['ChuShengNianFen']
Person['EducationLevel'] = House_Member['ZuiGaoXueLi']
Person['PersonType'] = House_Member['RenYuanLeiBie'].apply(RenYuanLeiBie_PROCESS)
Person['WorkerOrNot'] = Person['PersonType'].apply(WorkerOrNot_PROCESS)

Person['Occupation'] = Person['WorkerOrNot']*House_Member['ZhiYe']
Person['Occupation'] = Person['Occupation'].replace(np.nan, 0).astype('int')

Person['Industry'] = Person['WorkerOrNot']*House_Member['HangYe']
Person['Industry'] = Person['Industry'].replace(np.nan, 0).astype('int')

Person['LicenseType'] = House_Member['JiaZhaoLeiXing'].astype('int')

Person['SmartCardType'] = House_Member['GongJiaoPiaoZhengLeiXing'].astype('int')

Person['PhoneOperator'] = House_Member['ShouJiYunYingShang'].astype('int')

Person['WorkplaceOrSchool'] = Person['PersonType']* House_Member['DanWeiHuoXueXiao']
Person['WorkplaceOrSchool'] = Person['WorkplaceOrSchool'].apply(lambda x:2 if x in [6.0,8.0] else 1 if x in [1.0,2.0,3.0,4.0,5.0,7.0,9.0,10.0,12.0,16.0] else 0)



Person['WorkplaceOrSchoolAddr'] = House_Member['XiaoQuDaiMa'].apply(XIAOQU_DECODE,args=(district_dict,))+House_Member['XiangXiDizhi'].apply(_ADDRESS_CLEAN,args=(district_dict,))

if Decode:
    print('decode the address to locate')
    baidu_key = 'FhPo8GtDOmU9SMZFowSfYWGe9kR9hoCG'

    Person['WorkplaceOrSchoolTAZ'] = House_Member['XiaoQuDaiMa']
    #Person['RawdataofLocate'] = Person['WorkplaceOrSchoolAddr'].apply(GEOCODERS,args=(baidu_key,))
    Person['RawdataofLocate'] = Person['WorkplaceOrSchoolAddr'].apply_parallel(GEOCODERS,num_processes=30)
    #Person['RawdataofLocate'] = Person['WorkplaceOrSchoolAddr'].apply(GEOCODERS)

    Person['WorkplaceOrSchoolLat'] = Person['RawdataofLocate'].apply(WorkplaceOrSchoolLat_PROCESS)

    Person['WorkplaceOrSchoolLon'] = Person['RawdataofLocate'].apply(WorkplaceOrSchoolLon_PROCESS)
else:
    Decode_data = pd.read_csv('../documents/OutputFiles-PersonLevel_with_geodecode_check.csv')
    Person['RawdataofLocate'] = Decode_data['RawdataofLocate']
    Person['WorkplaceOrSchoolLat'] = Decode_data['WorkplaceOrSchoolLat']

    Person['WorkplaceOrSchoolLon'] = Decode_data['WorkplaceOrSchoolLon']



if Address_check:
    print('address check')
    Person['Rawdataofcheck'] = Person[['WorkplaceOrSchoolLon','WorkplaceOrSchoolLat','WorkplaceOrSchoolTAZ']].apply_parallel(_TAZ_CHECK,num_processes=30,static_data = [Map_data])
    Person['WorkplaceOrSchoolTAZ_predict'] = Person['Rawdataofcheck'].apply(lambda x:x[0])
    Person['DistWithTAZandTAZpredict'] = Person['Rawdataofcheck'].apply(lambda x:x[2])
    #Person['test'] = Person.apply(lambda x:_TAZ_CHECK1(x['WorkplaceOrSchoolLon'],x['WorkplaceOrSchoolLat'],x['WorkplaceOrSchoolTAZ']), axis=1)
else:
    Decode_data = pd.read_csv('../documents/OutputFiles-PersonLevel_with_geodecode_check.csv')
    Person['Rawdataofcheck'] = Decode_data['Rawdataofcheck']
    Person['WorkplaceOrSchoolTAZ_predict'] =  Decode_data['WorkplaceOrSchoolTAZ_predict']
    Person['DistWithTAZandTAZpredict'] =  Decode_data['DistWithTAZandTAZpredict']



print('Filename: {}. Save_name:{}'.format(Save_name,Save_path))
print('Run time: {}'.format(time.time()-Start_time))
Person.to_csv(Save_path,sep='\t',index=None)
Person.to_csv('../documents/OutputFiles-PersonLevel_with_geodecode_check.csv')
