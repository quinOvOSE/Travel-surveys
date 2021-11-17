import pandas as pd
import os
from Data_clean_process import ADDRESS_CLEAN, DATA_CLEAN

def DISTRICT_DECODE(district_no,district_dict):
    return district_dict[district_no]

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

district_dict = {1:'东城区',2:'西城区',3:'朝阳区',4:'丰台区',5:'石景山区',6:'海淀区',7:'房山区',8:'通州区',9:'顺义区',10:'昌平区',11:'大兴区',12:'门头沟区',13:'怀柔区',14:'平谷区',15:'密云区',16:'延庆区'}

Cite,Travel,Vehicle,License_Plate,House_Member,House = DATA_CLEAN(Table_Cite,Table_Travel,Table_Vehicle,Table_License_Plate,Table_House_Member,Table_House)

# input locate data
Locate_path = '../data/baiduToWgs_add_distance.csv'
Locate_data = pd.read_csv(Locate_path)

Save_dir = '../documents/'
Save_name ='FamilyBasicInformation.txt'
Save_path = os.path.join(Save_dir,Save_name)

House_output = pd.DataFrame()

House_output['FamilyID'] = House['JiaTingID']
House_output['HomeAddress'] ='北京市'+House['SuoShuChengQu'].apply(DISTRICT_DECODE,args=(district_dict,))+ House['DiZhi'].apply(ADDRESS_CLEAN,args=(district_dict,))
House_output['HomeLat'] = Locate_data['lat84']
House_output['HomeLon'] = Locate_data['lon84']
House_output['HomeTAZ'] = House['XiaoQuBianHao'].astype('int')
House_output['CarNum'] = House['YongYouXiaoQiCheShuLiang']
House_output['PermnResidNum'] = House['ChanZhuRenYuan']
House_output['WorkerNum'] = House['GongZuoYouJiRen']
House_output['DistrictIndex'] = House['SuoShuChengQu']
House_output['HousingType'] = House['ZhuFangLeiXing'].astype('int')
House_output['HousingArea'] = House['JianZhuMianJi']
House_output['HouseholdIncomeIndex'] = House['QuNianNianShouRu']
House_output['BikeNum'] = House['JiaoTaZiXingCheShuLiang']
House_output['E-bikeNum'] = House['DianDongZiXingCheShuLiang']
House_output['MotorbikeNum'] = House['MoTuoCheShuLiang']
House_output['ShiFouCanYuYaoHao'] = House['ShiFouCanYuYaoHao']
House_output.loc[House_output['ShiFouCanYuYaoHao']==1,'PartiLotteryOrNot']=1
House_output.loc[House_output['ShiFouCanYuYaoHao']==2,'PartiLotteryOrNot']=0
del House_output['ShiFouCanYuYaoHao']
House_output['TAZ_Num_predicted'] = Locate_data['predict_taz']
House_output['Distance_between_HomeTAZ_and_TAZ_Num_predicted'] = Locate_data['distance_between_taz_and_real_taz']
print('Filename: {}. Save_name:{}'.format(Save_name,Save_path))
House_output.to_csv(Save_path,sep='\t',index=None)
House_output.to_csv('../documents/FamilyBasicInformation.csv',index=None)
