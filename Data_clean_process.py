#!/usr/bin/python
# -*- coding:utf-8 -*-
import pandas as pd



def DATA_CLEAN(Table_Cite,Table_Travel,Table_Vehicle,
               Table_License_Plate,
               Table_House_Member,
               Table_House):
    print('--------------CLEAN HOUSE NO-----------------')
    # 忽略150101100040和80001001335两个家庭
    print('忽略150101100040和80001001335两个家庭')

    print('--------------CLEAN QUHAO NO-----------------')

    Table_License_Plate = Table_License_Plate.drop(index=list(Table_License_Plate.index[Table_License_Plate['JiaTingID']==150101100040])[0])
    Table_License_Plate = Table_License_Plate.drop(index=list(Table_License_Plate.index[Table_License_Plate['JiaTingID']==80001001335])[0])
    #对上述编号进行替换
    zone_id_clean_dict = {33000:330000,62010:62001,70816:70916,50600:52504,
                      50814:50703,63371:63316,71704:121131,10600:10606,
                      60200:60216,60470:60407,110108:121118,110203:100103,
                      40807:40401,106400:64000}
    print('在<家庭成员表>中，进行如下替换')
    for i in range(len(Table_House_Member['XiaoQuDaiMa'])):
        if Table_House_Member['XiaoQuDaiMa'].loc[i] in zone_id_clean_dict:
            print('将{}替换为{}'.format(Table_House_Member['XiaoQuDaiMa'].loc[i],
                                    zone_id_clean_dict[Table_House_Member['XiaoQuDaiMa'].loc[i]]))
            Table_House_Member['XiaoQuDaiMa'].loc[i] = zone_id_clean_dict[Table_House_Member['XiaoQuDaiMa'].loc[i]]

    print('在<家庭背景资料表>中，进行如下替换')
    for i in range(len(Table_House['XiaoQuBianHao'])):
        if Table_House['XiaoQuBianHao'].loc[i] in zone_id_clean_dict:
            print('将{}替换为{}'.format(Table_House['XiaoQuBianHao'].loc[i],
                                    zone_id_clean_dict[Table_House['XiaoQuBianHao'].loc[i]]))
            Table_House['XiaoQuBianHao'].loc[i] = zone_id_clean_dict[Table_House['XiaoQuBianHao'].loc[i]]

    print('在<家庭成员出行地点表>中，进行如下替换')
    for i in range(len(Table_Cite['DaoDaDiDianXiaoQuHao'])):
        if Table_Cite['DaoDaDiDianXiaoQuHao'].loc[i] in zone_id_clean_dict:
            print('将{}替换为{}'.format(Table_Cite['DaoDaDiDianXiaoQuHao'].loc[i],
                                    zone_id_clean_dict[Table_Cite['DaoDaDiDianXiaoQuHao'].loc[i]]))
            Table_Cite['DaoDaDiDianXiaoQuHao'].loc[i] = zone_id_clean_dict[Table_Cite['DaoDaDiDianXiaoQuHao'].loc[i]]

    print('在<家庭成员出行表>中，进行如下替换')
    for i in range(len(Table_Travel['QiTaDiFangXiaoQuhao'])):
        if Table_Travel['QiTaDiFangXiaoQuhao'].loc[i] in zone_id_clean_dict:
            print('将{}替换为{}'.format(Table_Travel['QiTaDiFangXiaoQuhao'].loc[i],
                                    zone_id_clean_dict[Table_Travel['QiTaDiFangXiaoQuhao'].loc[i]]))
            Table_Travel['QiTaDiFangXiaoQuhao'].loc[i] = zone_id_clean_dict[Table_Travel['QiTaDiFangXiaoQuhao'].loc[i]]

    return (Table_Cite,Table_Travel,Table_Vehicle,Table_License_Plate,Table_House_Member,Table_House)


# 输入
'''
Table_Cite_path = '../家庭成员出行地点表.csv'
Table_Travel_path = '../家庭成员出行表.csv'
Table_Vehicle_path = '../家庭成员拥有机动车情况表.csv'
Table_License_Plate_path = '../家庭成员汽车摇号表.csv'
Table_House_Member_path = '../家庭成员表.csv'
Table_House_path = '../家庭背景资料表.csv'

Table_Cite = pd.read_csv(Table_Cite_path)
Table_Travel = pd.read_csv(Table_Travel_path)
Table_Vehicle = pd.read_csv(Table_Vehicle_path)
Table_License_Plate = pd.read_csv(Table_License_Plate_path)
Table_House_Member = pd.read_csv(Table_House_Member_path)
Table_House = pd.read_csv(Table_House_path)

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



print(62001 in list(Cite['DaoDaDiDianXiaoQuHao']))
'''
