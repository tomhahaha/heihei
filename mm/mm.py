from DbCommon import mysql2pd
conn = mysql2pd('140.143.161.111', '3306', 'mm', 'root', 'a091211')
conn.write2mysql(conn.doget("select distinct * from poi").drop_duplicates(['id']),'poi',if_exists='replace')
conn.write2mysql(conn.doget("select distinct * from poi_data").drop_duplicates(['daytime','poiid']),'poi_data',if_exists='replace')
conn.close()
# def getdata():
#     sql1='''
#     select distinct * from poi
#     '''
#     sql2='''
#     select distinct * from poi_data
#     '''
#     res1=conn.doget(sql1)
#     res2=conn.doget(sql2).drop_duplicates(['DAYTIME','POIID'])
#     return res1,res2
# def write2table(df1,df2):
#     conn.write2mysql(df1,'poi')
#     conn.write2mysql(df2,'poi_data')
# if __name__=='__main__':
#     write2table(getdata())