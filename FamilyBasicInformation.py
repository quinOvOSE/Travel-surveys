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
district_dict = {1:'东城区',2:'西城区',3:'朝阳区',4:'丰台区',5:'石景山区',6:'海淀区',7:'房山区',8:'通州区',9:'顺义区',10:'昌平区',11:'大兴区',12:'门头沟区',13:'怀柔区',14:'平谷区',15:'密云区',16:'延庆区'}

Cite,Travel,Vehicle,License_Plate,House_Member,House = DATA_CLEAN(Table_Cite,Table_Travel,Table_Vehicle,Table_License_Plate,Table_House_Member,Table_House)

# input locate data
Locate_path = '../data/baiduToWgs_add_distance.csv'
Locate_data = pd.read_csv(Locate_path)

Save_dir = '../documents/'
Save_name ='OutputFiles-FamilyLevel.txt'
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
