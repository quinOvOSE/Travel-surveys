import pandas as pd
import os
from Data_clean_process import DATA_CLEAN

def DistrictName_PROCESS(ID):
    dicts = {1:'Dongcheng',2:'Xicheng',3:'Chaoyang',
             4:'Fengtai',5:'Shijiingshan',6:'Haidian',
             7:'Fangshan',8:'Tongzhou',9:'Shunyi',
             10:'Changping',11:'Daxing',12:'Mengtougou',
             13:'Huairou',14:'Pinggu',15:'Miyun',16:'Yanqing'}
    return dicts[ID]

def DistrictCategory_PROCESS(name):
    if name in ['Dongcheng', 'Xicheng', 'Chaoyang', 'Fengtai', 'Shijiingshan', 'Haidian']:
        return 'CentralAreas'
    elif name in ['Fangshan', 'Tongzhou', 'Shunyi', 'Changping', 'Daxing', 'Mengtougou']:
        return 'Suburbs'
    elif name in ['Huairou', 'Pinggu', 'Miyun', 'Yanqing']:
        return 'OuterSuburbs'
    else:
        print('ERROE happened in DistrictCategory_PROCESS')

def HouseholdIncome_PROCESS(ID):
    dicts = {1:25000,2:75000,3:125000, 4:175000, 5:225000,6:275000,7:325000, 8:550000}
    return dicts[ID]



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

# load data from FamilyBasicInformation
BasicInformation = pd.read_csv('../documents/FamilyBasicInformation.csv')






Save_dir = '../documents/'
Save_name ='FamilyAdvancedformation.txt'
Save_path = os.path.join(Save_dir,Save_name)


HouseAdvanced = pd.DataFrame()
HouseAdvanced['FamilyID'] = BasicInformation['FamilyID']
HouseAdvanced['HomeAddress'] = BasicInformation['HomeAddress']
HouseAdvanced['HomeLat'] = BasicInformation['HomeLat']
HouseAdvanced['HomeLon'] = BasicInformation['HomeLon']
HouseAdvanced['HomeTAZ'] = BasicInformation['HomeTAZ']
HouseAdvanced['CarNum'] = BasicInformation['CarNum']
HouseAdvanced['PermnResidNum'] = BasicInformation['PermnResidNum']

HouseAdvanced['MemberNum'] = HouseAdvanced['FamilyID'].apply(
    lambda x:len(House_Member[House_Member['JiaTingID']==x])
)
HouseAdvanced['ChildNum'] = HouseAdvanced['FamilyID'].apply(
    lambda x:len(House_Member[(House_Member['ChuShengNianFen']>1996)&(House_Member['JiaTingID']==x)]))

HouseAdvanced['ElderNum'] = HouseAdvanced['FamilyID'].apply(
    lambda x:len(House_Member[(House_Member['ChuShengNianFen']>=1954)&(House_Member['JiaTingID']==x)]))

HouseAdvanced['WorkerNum'] = BasicInformation['WorkerNum']
HouseAdvanced['DistrictIndex'] = BasicInformation['DistrictIndex']

HouseAdvanced['DistrictName'] = HouseAdvanced['DistrictIndex'].apply(DistrictName_PROCESS)
HouseAdvanced['DistrictCategory'] = HouseAdvanced['DistrictName'].apply(DistrictCategory_PROCESS)

HouseAdvanced['HousingType'] = BasicInformation['HousingType']
HouseAdvanced['HousingArea'] = BasicInformation['HousingArea']
HouseAdvanced['HouseholdIncomeIndex'] = BasicInformation['HouseholdIncomeIndex']
HouseAdvanced['HouseholdIncome'] = HouseAdvanced['HouseholdIncomeIndex'].apply(HouseholdIncome_PROCESS)

HouseAdvanced['BikeNum'] = BasicInformation['BikeNum']
HouseAdvanced['E-bikeNum'] = BasicInformation['E-bikeNum']
HouseAdvanced['MotorbikeNum'] = BasicInformation['MotorbikeNum']
HouseAdvanced['PartiLotteryOrNot'] = BasicInformation['PartiLotteryOrNot']

HouseAdvanced['LotteryPartiNum'] = HouseAdvanced['FamilyID'].apply(
    lambda x:len(License_Plate[License_Plate['JiaTingID']==x])
)

HouseAdvanced['LotteryWinNum'] = HouseAdvanced['FamilyID'].apply(
    lambda x:len(License_Plate[(License_Plate['JiaTingID']==x)&(License_Plate['ShiFouZhongQian']==1)])
)


print('Filename: {}. Save_name:{}'.format(Save_name,Save_path))
HouseAdvanced.to_csv(Save_path,sep='\t',index=None)
HouseAdvanced.to_csv('../documents/FamilyAdvancedformation.csv',index=None)
