import requests
import re,time
import pandas as pd
from bs4 import BeautifulSoup
import json
from DbCommon import mysql2pd

def getcookie():
    cookie1="key=1daea98643e297f2c6b7c14a3b74e630;guid=79b2-f49d-fe37-7760;UM_distinctid=164daa6cd8a41d-0e8d538a282845-16396952-fa000-164daa6cd8b62f;CNZZDATA1259319723=1622084908-1532675501-null%7C1532675501;_uab_collina=153267672299386011087579;_umdata=0712F33290AB8A6D7A82809DCDBDF23582624AEA973E56CA5E32F74F69F0B2E633A7BE54B94CA04CCD43AD3E795C914C91A5363412716E14537180ABD9B760A9;passport_login=MjA4OTczNzM3LGFtYXBfMTg4MTMxNzI5NjVCeUphMUIxSkIsczNpbmFwOXNqYTU0NXJ4b2RhMWpqOTJ3YzVwenRoZ3gsMTUzMjY3Njc0NSxOV1EwWTJGaU5XVm1OakkwTnpNMU1UazBOVE5pWVRGaFpHSXdZVFF5TWpBPQ%3D%3D"
    cookie_dic={}
    for l in cookie1.split('; '):
        xx=l.split('=')
        cookie_dic[xx[0]]=xx[1]
    return cookie_dic
headers = {
        'Accept':'application/json,text/javascript,*/*;q=0.01',
        'Referer':'http://i.amap.com/detail/B000A830DN?adcode=110000&keyword=%E5%8C%97%E4%BA%AC%E6%9E%97%E4%B8%9A%E5%A4%A7%E5%AD%A6',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_13_4)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
s=requests.session()
cook=getcookie()

def getIdList(type):
    base_url="http://restapi.amap.com/v3/place/text?&keywords=thisplace&city=%E5%8C%97%E4%BA%AC&output=json&offset=50&page=thispage&key=9f99fc570ccaf6abc209780433d9f4c1&extensions=all"
    getCount_url=base_url.replace('thisplace',type).replace('thispage','1')
    respon=str(s.get(getCount_url,headers=headers,cookies=cook,verify = False).text)
    n=int(respon.split('''"count":"''')[1].split('''","info''')[0])
    i=1
    res = []
    while i<=n//50:
        print(str(i))
        getData_url = base_url.replace('thisplace', type).replace('thispage', str(i))
        data=json.loads(s.get(getData_url,headers=headers,cookies=cook,verify = False).text)["pois"]
        for d in data:
            one=[]
            for k in ["id","name","type","typecode","location","adname"]:
                if k == "location":
                    one.append(d.get(k).split(',')[0])
                    one.append(d.get(k).split(',')[1])
                else:
                    one.append(d.get(k))
            res.append(one)
        i+=1
    getData_url = base_url.replace('thisplace', type).replace('thispage', str(i))
    data = json.loads(s.get(getData_url, headers=headers, cookies=cook, verify=False).text)["pois"]
    for d in data:
        one = []
        for k in ["id", "name", "type", "typecode", "location", "adname"]:
            if k=="location":
                one.append(d.get(k).split(',')[0])
                one.append(d.get(k).split(',')[1])
            else:
                one.append(d.get(k))
        res.append(one)
    res=pd.DataFrame(res,columns=["id","name","type","typecode","location_x","location_y","adname"])
    res.to_csv('res.csv')
    return res
def getPOIdata(poiid,day,term):
    getData_url="http://i.amap.com/service/aoi-index?aoiids={}&end={}&offset={}&byhour=1&refresh=0".format(poiid,day,term)
    data=json.loads(s.get(getData_url, headers=headers, cookies=cook, verify=False).text)["data"][poiid]
    data=pd.DataFrame(data,columns=['daytime','x','y','value'])[['daytime','value']]
    data['poiid']=poiid
def getPoiList(conn):
    #清除旧数据
    conn.dopost("truncate table poi")
    # 获取POI的id，存入数据库
    for term in ["餐厅"]:
        data = getIdList(term)
        conn.write2mysql(data, 'poi')
if __name__=='__main__':
    conn = mysql2pd('140.143.161.111', '3306', 'mm', 'root', 'a091211')
    # getPoiList(conn)
    poi_list=conn.doget("select distinct id from poi")['POI'].values
    for id in poi_list:
        conn.write2mysql(getPOIdata(id),'poi_data')
    conn.close()

