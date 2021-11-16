import pandas as pd
import numpy as np
import os
from Data_clean_process import ADDRESS_CLEAN, DATA_CLEAN
#from

def _ADDRESS_CLEAN(address,district_dict):
    if pd.isnull(address) ==True:
        return '无地址'
    if address in ['※※', '※※※']:
        return '无地址'
    else:
        tt =  ADDRESS_CLEAN(address,district_dict)
        return tt


def XIAOQU_DECODE(code,district_dict):
    if pd.isnull(code) ==False:
        if int(code) == 999999:
            return '京外'
        if len(str(int(code))) == 5:
            return '北京市'+district_dict[int(str(int(code))[0])]

        elif len(str(int(code))) == 6:
            return '北京市'+district_dict[int(str(int(code))[:2])]

        else:
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

def WorkerOrNot_PROCESS(num):
    if num ==1 or num ==2:
        return 1
    else:
        return 0

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

district_dict = {1:'西城区',2:'东城区',3:'东城区',4:'西城区',5:'海淀区',
6:'朝阳区',7:'丰台区',8:'石景山区',9:'昌平区',10:'顺义区',11:'通州区',
12:'大兴区',13:'房山区',14:'门头沟区',15:'延庆区',16:'怀柔区',17:'密云区',18:'平谷区'}

Cite,Travel,Vehicle,License_Plate,House_Member,House = DATA_CLEAN(Table_Cite,Table_Travel,Table_Vehicle,Table_License_Plate,Table_House_Member,Table_House)



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

Person['WorkplaceOrSchoolTAZ'] = House_Member['XiaoQuDaiMa']
