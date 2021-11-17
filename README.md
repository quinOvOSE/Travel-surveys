# Travel-surveys
1. 数据清洗

2. 

PS 在pd中使用多进程
```markdown
# multiprocesspandas import applyparallel
#如果只有单一输入WorkplaceOrSchoolAddr
Person['RawdataofLocate'] = Person['WorkplaceOrSchoolAddr'].apply_parallel(GEOCODERS,num_processes=30)
#如果输入是多列
#df是输入的dataframe,static_data是额外的输入
def _TAZ_CHECK(df,static_data):
    p = [df['WorkplaceOrSchoolLon'],df['WorkplaceOrSchoolLat']]
    code = df['WorkplaceOrSchoolTAZ']
    output = LOCATE_CHECK(p,code,static_data[0])
    return output
    
Person['Rawdataofcheck']=Person[['WorkplaceOrSchoolLon','WorkplaceOrSchoolLat','WorkplaceOrSchoolTAZ']].apply_parallel(_TAZ_CHECK,num_processes=30,static_data = [Map_data])


