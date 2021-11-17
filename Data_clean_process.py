#!/usr/bin/python
# -*- coding:utf-8 -*-
import pandas as pd

def ADDRESS_CLEAN(i,district_dict):
    #1.删掉中文字符前的所有数字和英文字符。其中存在'2020年''旧地址''抽中\失'等字样，也去掉
    #2.删掉海淀区等字样，但是若出现“海淀”两字不删，可能有小区以区名为开头，所以不删。

    first_num_check = True if u'\u4e00' <= i[0] <= u'\u9fff' and i[0] not in ['年','抽','失','中','旧','地','址'] else False

    while(first_num_check==False):
        i = i[1:]
        first_num_check = True if u'\u4e00' <= i[0] <= u'\u9fff' and i[0] not in ['年','抽','失','中','旧','地','址'] else False

    if i[:3] in list(district_dict.values()):
        i = i[3:]
    if i[:4] in  list(district_dict.values()):
        i = i[4:]

    return i


def DATA_CLEAN(Table_Cite,Table_Travel,Table_Vehicle,
               Table_License_Plate,
               Table_House_Member,
               Table_House):
    print('--------------CLEAN HOUSE NO-----------------')
    # 忽略150101100040和80001001335两个家庭
    print('忽略150101100040和80001001335两个家庭')

    Table_License_Plate = Table_License_Plate.drop(index=list(Table_License_Plate.index[Table_License_Plate['JiaTingID']==150101100040])[0])
    Table_License_Plate = Table_License_Plate.drop(index=list(Table_License_Plate.index[Table_License_Plate['JiaTingID']==80001001335])[0])

    print('--------------CLEAN QUHAO NO-----------------')

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

    print('--------------CLEAN ADDRESS-----------------')

    #1. Clean Table_House
    print('Clean the address in Table_House')
    Table_House_address_clean = {'qnhbl8-2-502':'青年湖北里6-5-101','12-1-2208':'芳群园一区5#-1409','1-2-303':'芳群园一区1109','07150520#5-201':'角门东里一社区20#2-401','070703':'开阳里三区1-5号1-1508','31-2-303':'大兴区富强东里7-5-403','19-3-101':'大兴区富强东里8-5-502','57-1-201':'加州水郡东区57-1-201','66-1-601':'加州水郡东区66-1-601','56-5-501':'加州水郡东区56-5-501','69-2-802':'加州水郡东区69-2-802','69-3-802':'加州水郡东区69-3-802','69-5-701':'加州水郡东区69-5-701','68-1-601':'加州水郡东区68-1-601','8-3-602':'凯旋大街8-3-602','8-5-102':'昌平区城北万科16-1-401','25#-2-102':'煤炭科技苑社区25#-2-102','31#-601':'煤炭科技苑社区31#-601','268hao':'石各庄村268号','21-5-562':'太平路12北1-133','21-2-6':'海淀区苗甫2门5','0510067#-4-502':'海淀区建清小区1#-14-402','3#-10-401':'青年楼3#-10-401','6-7-202':'苹一区2-16（2-1-601）','26-1-402':'苹果园街道苹一区26-8-502','8-1-301':'苹果园街道苹四区11-103','10-1-804':'苹果园苹四区','9-107':'苹果园苹四区','4-3-201':'西黄新村北星2-907','8-6-301':'苹果园街道苹四区6-70','中18-2-301':'模式口中里18-2-301','中33-1-102':'模式口中里33-1-102','中39-8-202':'模式口中里39-8-202','中38-3-201':'模式口中里38-3-201','中3-1-201':'模式口中里3-1-201','中33-1-302':'模式口中里33-1-302','中18-2-502':'模式口中里18-2-502','中17-2-201':'模式口中里17-2-201','33-1-502':'模式口南里33-1-502','44-1-601':'永乐西区44-1-601','22-2-602':'永乐西区22-2-602','20-8-501':'五芳园20-8-501','26-3-601':'五芳园26-3-601','20-1-103':'五芳园20-1-103','21-5-101':'五芳园21-5-101','28-6-201':'五芳园28楼6门201号','12-7-102':'依翠园12-7-102','4#032':'广外三义东里4#032','26-3-302': '马坡佳和宜园26-3-302'}

    for key,value in Table_House_address_clean.items():
        Table_House['DiZhi'].replace(key,value,inplace=True)



    # Clean House_Member
    #print(Table_House_Member[Table_House_Member['XiangXiDizhi']=='石景山苹果园新生活']['XiaoQuDaiMa'])
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='石景山苹果园新生活','XiaoQuDaiMa']=80303
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='阜成门外大街','XiaoQuDaiMa']=10601
    #print(Table_House_Member[Table_House_Member['XiangXiDizhi']=='石景山苹果园新生活']['XiaoQuDaiMa'])

    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='165中','XiangXiDizhi']='第一六五中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='94中','XiangXiDizhi']='第九十四中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='145中','XiangXiDizhi']='第一四五中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='22中','XiangXiDizhi']='第二十二中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='154中','XiangXiDizhi']='第一五四中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='161中','XiangXiDizhi']='第一六一中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='62中','XiangXiDizhi']='第六十二中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='63中','XiangXiDizhi']='第六十三中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='15中','XiangXiDizhi']='第十五中学'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='43中','XiangXiDizhi']='第四十三中学'

    Table_House_Member.loc[Table_House_Member['XiaoQuDaiMa']==107,'XiaoQuDaiMa']=50107



    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='8-3-602','XiangXiDizhi']='良乡西潞园四里8号3单元602'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='82-3-501','XiangXiDizhi']='良乡西潞园四里82号3单元501'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='84-5-401','XiangXiDizhi']='良乡西潞园四里84号5单元401'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='798','XiangXiDizhi']='七九八艺术区'
    Table_House_Member.loc[Table_House_Member['XiangXiDizhi']=='5-1-601','XiangXiDizhi']='北京市朝阳区十里堡南里中路'


    return (Table_Cite,Table_Travel,Table_Vehicle,Table_License_Plate,Table_House_Member,Table_House)




# 输入
if __name__ == '__main__':
    Table_Cite_path = '../data/家庭成员出行地点表.csv'
    Table_Travel_path = '../data/家庭成员出行表.csv'
    Table_Vehicle_path = '../data/家庭成员拥有机动车情况表.csv'
    Table_License_Plate_path = '../data/家庭成员汽车摇号表.csv'
    Table_House_Member_path = '../data/家庭成员表.csv'
    Table_House_path = '../data/家庭背景资料表.csv'

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
