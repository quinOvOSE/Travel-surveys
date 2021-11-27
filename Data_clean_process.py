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



    #'121502001937_2'这位出行者的第一个活动地点和家距离1km，但他凌晨三点写的在单位，且没有写单位地址，45年人，把凌晨三点地点改为家。
    Table_Travel.loc[(Table_Travel['JiaTingID']==121502001937)&(Table_Travel['ChengYuanID']==2),'LingChen3DianZaiNa']=1
    #'161602000268_1'删掉这个人的出行行为
    temp = Table_Travel[(Table_Travel['JiaTingID']==161602000268)&(Table_Travel['ChengYuanID']==1)].index
    Table_Travel = Table_Travel.drop(temp)
    #'63504003331_2'这位出行者的第一个活动地点和家距离2km，但他凌晨三点写的在单位，且没有写单位地址，把凌晨三点地点改为家。
    Table_Travel.loc[(Table_Travel['JiaTingID']==63504003331)&(Table_Travel['ChengYuanID']==2),'LingChen3DianZaiNa']=1

    #'52502002589_3'删掉这个人的出行行为
    temp = Table_Travel[(Table_Travel['JiaTingID']==52502002589)&(Table_Travel['ChengYuanID']==3)].index
    Table_Travel = Table_Travel.drop(temp)

    #'80601001405_1'删掉这个人的出行行为
    temp = Table_Travel[(Table_Travel['JiaTingID']==80601001405)&(Table_Travel['ChengYuanID']==1)].index
    Table_Travel = Table_Travel.drop(temp)

    #‘20503000743_2’这个人在Cite表格离开事件有问题，他的第45条出行数据都是不离开，去掉第五条
    temp = Table_Cite[(Table_Cite['JiaTingID']==20503000743)&(Table_Cite['ChengYuanID']==2)&(Table_Cite['DiDianID']==5)].index
    Table_Cite = Table_Cite.drop(temp)

    #‘20301001021_1’这个人在Cite表格离开事件有问题，他的第23条出行数据都是不离开，但时间只有一个，去掉该人的出行
    temp = Table_Travel[(Table_Travel['JiaTingID']==20301001021)&(Table_Travel['ChengYuanID']==1)].index
    Table_Travel = Table_Travel.drop(temp)

    #以下人的出行地点数据有问题，删除，需要检查

    temp = Table_Travel[(Table_Travel['JiaTingID']==20301001021)&(Table_Travel['ChengYuanID']==1)].index
    Table_Travel = Table_Travel.drop(temp)

    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20103001251)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70910004310)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71427004622)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121303000912)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120301001531)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121703002210)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121408002720)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121313000721)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121306000858)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121306000857)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120700001403)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==171902000435)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==171902000442)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==172004000076)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181101000242)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181101000249)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181608000288)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161503000145)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131809000181)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131809000159)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131809000065)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132021001339)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132023001301)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131701001217)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131701001190)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132109000849)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131400000596)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63602000383)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61703000727)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61701000765)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61502000910)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62403001841)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61404003062)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63504003327)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52102000053)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52102000059)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51206004716)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50608002364)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80104000024)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80301001021)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80601001471)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80402001654)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80903001704)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80901001921)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10306000284)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==40200001791)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110300002399)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110901002544)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111201000535)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111204000708)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110503001886)&(Table_Travel['ChengYuanID']==5)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==141003000455)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==141201000638)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==102401000280)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==102401000218)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==101501001366)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==101501001378)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==101501001396)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==101400001352)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30203002163)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30102002413)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70904002239)&(Table_Travel['ChengYuanID']==1)].index)

    # 需要检查，可能的错误是他们在出行中工作或学校，但是没有对应地址
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20802000383)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20802000399)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==21007000183)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==21007000183)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==21007000186)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000210)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000212)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000213)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000217)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000218)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000229)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000237)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20902000260)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20802000478)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20701000561)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20503000741)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20503000755)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20502000796)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20504000837)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20503000842)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20503000844)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20503000855)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20301001020)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20201001329)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20201001163)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20102001317)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20402001464)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20601001619)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20603001696)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20603001696)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20604001825)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30201002211)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30201002227)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30201002233)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30201002234)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30102002338)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30102002359)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30702002464)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30702002470)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30702002545)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30604002970)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==30604002970)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==20401001411)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000008)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000010)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000027)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000027)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000081)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000089)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000098)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70704000117)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70703000204)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70703000204)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70810000282)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70803000493)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70407000730)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70916002093)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70112001211)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70608001655)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70608001676)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70606001725)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70605001808)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70909001962)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70907002173)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71606002510)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71707003300)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71703003350)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71703003426)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71002003557)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71002003627)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71002003629)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71404004465)&(Table_Travel['ChengYuanID']==5)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71434004550)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70113004813)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70113004829)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70109004890)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70109004893)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71105004925)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71203004998)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71203004978)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71203004970)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71203004965)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71203004961)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71110005003)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71110005019)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71110005030)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71110005032)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71110005037)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71110005039)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71301005132)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71301005144)&(Table_Travel['ChengYuanID']==6)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71301005145)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70918004410)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70918004412)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70110001139)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70302003940)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70203001241)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70406000836)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71507003905)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70603001452)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71703003374)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70609001711)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71105003154)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71105003158)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71419002968)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71419002983)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71103005098)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71103005108)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70303001192)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70503000532)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70105001083)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70105001106)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70105001113)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71504003722)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71504003723)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71504003721)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71504003739)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71504003742)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70916002074)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70916002076)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71205003257)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==70916005281)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71707003447)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71707003448)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71707003462)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71707003463)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==71707003473)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120500001288)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120301001526)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121128000215)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120201002982)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121120000089)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121121000167)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121408002690)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121408002715)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121703002800)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121703002775)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121703002835)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121804002876)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121212000294)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121211000330)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121203000527)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121203000533)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121203000535)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121203000547)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121311000824)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121306000859)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121306000855)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121015000992)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120801001061)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120602001246)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120602001250)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120602001276)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120501001347)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120900001682)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120900001683)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120900001683)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120900001686)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==120900001743)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==121214000604)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==170600000648)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==170600000660)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==171902000424)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==171902000439)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==172004000044)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==172004000045)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181702000025)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181702000031)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181702000031)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181702000033)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181702000036)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181701000120)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181101000207)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181604000336)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==180300000471)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==180300000471)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181502000546)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==181200000586)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==150101000414)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==150101000426)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==150303000522)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==150304000567)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==150304000573)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161501000002)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161501000010)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161403000375)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161104000440)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161104000483)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161207000574)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161407000092)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161602000201)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==161602000285)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132303000374)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132502000316)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132702000249)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131809000023)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131701001206)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132806000923)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132806000933)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132215000788)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131400000537)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131400000558)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132109000848)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132216000816)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132215000761)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132215000768)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132209000743)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==132214000687)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131400000589)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==131400000521)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==91606000014)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==91602000161)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==91602000196)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90516000330)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90905000442)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90205000907)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90209000925)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90206000969)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90214001251)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90307001540)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90305001565)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90214001342)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==91302001387)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90305001596)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90305001596)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==90305001674)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==91000001922)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==91000001932)&(Table_Travel['ChengYuanID']==5)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61220004333)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62004000253)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61902000295)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63602000378)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63602000384)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60604000668)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61701000763)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61701000764)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61501000806)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61501000810)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63800001234)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61214004597)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60905001577)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60905001581)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62501002025)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62504002065)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62502002131)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62502002133)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62608002407)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62906002507)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63405002681)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==64107002753)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63602002825)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63505003253)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60106003453)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==62904003889)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63105004009)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==64205004105)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61313004217)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61310004272)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63204005123)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63211005547)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60410005583)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60410005600)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60409005625)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61205005928)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61206005983)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==61206006000)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==60206003777)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50406001857)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52102000071)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50302001599)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50401001688)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50401001692)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50601002044)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50603002201)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50603002219)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50604002307)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52805003004)&(Table_Travel['ChengYuanID']==5)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50505003750)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50505003774)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51206004685)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51206004708)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51206004712)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51206004713)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51206004715)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52803005763)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51812005371)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51812005371)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51903005409)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51903005427)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52803005777)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52803005779)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51506005862)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51506005872)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51410005934)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51410005945)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52207000936)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52505002416)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52503002448)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52503002472)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52503002473)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50503002553)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52502002630)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52502002637)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50905003993)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51903004528)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51820005555)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52410002749)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51901000376)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51901000379)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51901000386)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51901000394)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50101000459)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50101000545)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50101000553)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50401001663)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50406001915)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50601002139)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52502002587)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52505002663)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52402002694)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52702003255)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50504003812)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51207004767)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51207004779)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51207004787)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51605005277)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51802005457)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==52302001084)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50303001486)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50303001487)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==50303001518)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51202004604)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==51202004627)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80103000052)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80101000082)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80101000084)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80101000108)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80105000135)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80701000294)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80203000369)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80203000511)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80203000484)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80204000537)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80803000708)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80803000717)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80803000754)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80803000727)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80803000722)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80803000828)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80803000829)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80501000955)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80501000986)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80303001057)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80303001066)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80305001232)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80601001420)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80302001290)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80602001398)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80601000479)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80601001482)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80401001567)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80903001986)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80903001986)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80901001926)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==80901001924)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10306000216)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10604000038)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10703000384)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10704000428)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10704000435)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10506000684)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10506000681)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10509000883)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10510000947)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10404001042)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10402001085)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10602001398)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10205001591)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10208001745)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10208001755)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10208001755)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==40200001819)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==40602002326)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==40504002803)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==40502002926)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10702000519)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10702000519)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==40200001792)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==10205001675)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110301002433)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110100002722)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110917002688)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110401002910)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111302000034)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111304000146)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111402000430)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111106001495)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111106001495)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111506001251)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111106001514)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111205001556)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111106001694)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111105001725)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==111005001835)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110503001962)&(Table_Travel['ChengYuanID']==4)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110802002022)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110802002027)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==110901002583)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==140906000081)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==140906000109)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==141204000142)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==141204000181)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==141003000472)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==140400000530)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==140400000532)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==140814000642)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==140814000656)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==140822000708)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==141202000074)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==141202000074)&(Table_Travel['ChengYuanID']==5)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==100300001109)&(Table_Travel['ChengYuanID']==5)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==100204001040)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==102106000684)&(Table_Travel['ChengYuanID']==1)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==172006000006)&(Table_Travel['ChengYuanID']==3)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==63505003221)&(Table_Travel['ChengYuanID']==2)].index)
    Table_Travel = Table_Travel.drop(Table_Travel[(Table_Travel['JiaTingID']==40801002249)&(Table_Travel['ChengYuanID']==1)].index)



    #有一些到达单位和学校的人，没有出行目的，依据其的活动进行赋值
    Table_Cite.loc[(Table_Cite['JiaTingID']==171904000397)&(Table_Cite['ChengYuanID']==1)&(Table_Cite['DiDianID']==4),'ZaiNaGanShenMe'] = 3
    Table_Cite.loc[(Table_Cite['JiaTingID']==171904000413)&(Table_Cite['ChengYuanID']==4)&(Table_Cite['DiDianID']==4),'ZaiNaGanShenMe'] = 5
    Table_Cite.loc[(Table_Cite['JiaTingID']==131100001481)&(Table_Cite['ChengYuanID']==2)&(Table_Cite['DiDianID']==4),'ZaiNaGanShenMe'] = 3
    Table_Cite.loc[(Table_Cite['JiaTingID']==91000001925)&(Table_Cite['ChengYuanID']==1)&(Table_Cite['DiDianID']==4),'ZaiNaGanShenMe'] = 3
    Table_Cite.loc[(Table_Cite['JiaTingID']==50303001465)&(Table_Cite['ChengYuanID']==3)&(Table_Cite['DiDianID']==4),'ZaiNaGanShenMe'] = 5
    Table_Cite.loc[(Table_Cite['JiaTingID']==80301001014)&(Table_Cite['ChengYuanID']==3)&(Table_Cite['DiDianID']==4),'ZaiNaGanShenMe'] = 3
    Table_Cite.loc[(Table_Cite['JiaTingID']==111109000846)&(Table_Cite['ChengYuanID']==3)&(Table_Cite['DiDianID']==4),'ZaiNaGanShenMe'] = 3



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
'''
#以下人的出行地点数据有问题，删除，需要检查
20103001251_1
30203002163_1
30102002413_1
70904002239_1
70910004310_1
71427004622_2
121303000912_1
120301001531_1
121703002210_1
121408002720_2
121313000721_3
121306000858_2
121306000857_1
120700001403_2
171902000435_3
171902000442_1
172004000076_2
181101000242_1
181101000249_1
181608000288_3
161503000145_3
131809000181_2
131809000159_1
131809000065_2
132021001339_4
132023001301_1
131701001217_3
131701001190_2
132109000849_1
131400000596_2
63602000383_1
61703000727_3
61701000765_3
61502000910_1
62403001841_1
61404003062_2
63504003327_1
52102000053_4
52102000059_1
51206004716_1
50608002364_1
80104000024_1
80301001021_3
80601001471_1
80402001654_1
80903001704_2
80901001921_2
10306000284_2
40200001791_1
110300002399_2
110901002544_3
111201000535_1
111204000708_2
110503001886_5
141003000455_1
141201000638_1
102401000280_1
102401000218_1
101501001366_2
101501001378_2
101501001396_1
101400001352_1



20103001251_1
70910004310_1
71427004622_2
121303000912_1
120301001531_1
121703002210_1
121408002720_2
121313000721_3
121306000858_2
121306000857_1
120700001403_2
171902000435_3
171902000442_1
172004000076_2
181101000242_1
181101000249_1
181608000288_3
161503000145_3
131809000181_2
131809000159_1
131809000065_2
132021001339_4
132023001301_1
131701001217_3
131701001190_2
132109000849_1
131400000596_2
63602000383_1
61703000727_3
61701000765_3
61502000910_1
62403001841_1
61404003062_2
63504003327_1
52102000053_4
52102000059_1
51206004716_1
50608002364_1
80104000024_1
80301001021_3
80601001471_1
80402001654_1
80903001704_2
80901001921_2
10306000284_2
40200001791_1
110300002399_2
110901002544_3
111201000535_1
111204000708_2
110503001886_5
141003000455_1
141201000638_1
102401000280_1
102401000218_1
101501001366_2
101501001378_2
101501001396_1
101400001352_1
30203002163_1
30102002413_1
70904002239_1

'''
