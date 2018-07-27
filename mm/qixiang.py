import requests
import re,time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def getcookie():
    cookie="PHPSESSID=c97nhgkb53aud2ef1vcubrj734; Hm_lvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1532262046; login_id_chat=0; pgv_pvi=7751745536; pgv_si=s5000892416; surveyCookie=0; userLoginKey=1825acb45ef0bbe8b69b44085a8d058e; trueName=%E6%9D%8E%E9%92%B0%E6%9B%BC; userName=E31DB4826D2B76BB76E13651ACBC15B2; login_name_chat=0; Hm_lpvt_d9508cf73ee2d3c3a3f628fe26bd31ab="+str(int(time.time()))
    cookie1="PHPSESSID=c97nhgkb53aud2ef1vcubrj734; Hm_lvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1532262046; login_id_chat=0; pgv_pvi=7751745536; pgv_si=s5000892416; surveyCookie=0; login_name_chat=0; Hm_lpvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1532334013; userLoginKey=1825acb45ef0bbe8b69b44085a8d058e; trueName=%E6%9D%8E%E9%92%B0%E6%9B%BC; userName=E31DB4826D2B76BB76E13651ACBC15B2"
    cookie_dic={}
    for l in cookie1.split('; '):
        xx=l.split('=')
        cookie_dic[xx[0]]=xx[1]
    return cookie_dic
def DirLogin(url,data_dict):
    login_url='https://data.cma.cn/user/Login.html'
    baseurl = 'http://data.cma.cn'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'data.cma.cn',
        'Origin': 'http://data.cma.cn',
        'Referer': 'http://data.cma.cn/dataService/cdcindex/datacode/A.0012.0001/show_value/normal.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_13_4)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36'
    }
    s=requests.session()
    driver = webdriver.PhantomJS('/Users/cloudin1/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
    driver.get("http://data.cma.cn/user/toLogin.html")
    # print(driver.page_source)
    # iframe = driver.find_elements_by_tag_name('iframe')[0]
    # driver.switch_to.frame(iframe)
    # print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    codeurl=baseurl+soup.find('img',{'id':'yw0'})['src']
    print(codeurl)
    valcode = requests.get(codeurl).content
    f = open('valcode.png', 'wb')
    # pic=valcode.split('''"imastr":"''')[1].split('''","''')[0].replace(r'\/','/').replace('\\n','').replace('\\r','')
    # print(pic)
    f.write(valcode)
    f.close()
    code = input('请输入验证码：')
    data={
        'userName':'1033042436%40qq.com',
        'password':'ok123456',
        'callback':'jQuery111007370453034824596_1532276846334',
        '_':str(int(time.time() * 1000))
    }
    data["verifyCode"] = str(code)
    rs=s.get(login_url,headers=headers,data=data)
    cook=rs.cookies
    cook=getcookie()
    # print(cook.items())
    rs=s.get('http://data.cma.cn/data/search.html?dataCode=A.0012.0001',headers=headers,cookies=cook,params=data_dict,verify = False)
    rs.encoding='utf-8'
    print(rs.text)
if __name__=='__main__':
    url='http://data.cma.cn/data/search.html?dataCode=A.0012.0001'
    data_str='''
    dateS: 2018-07-22 00
    dateE: 2018-07-22 23
    hidden_limit_timeRange: 7
    hidden_limit_timeRangeUnit: Day
    isRequiredHidden[]: dateS
    isRequiredHidden[]: dateE
    chooseType: Station
    isRequiredHidden[]: station_ids[]
    station_ids[]: 54398
    station_ids[]: 54399
    station_ids[]: 54406
    station_ids[]: 54416
    station_ids[]: 54419
    station_ids[]: 54421
    station_ids[]: 54424
    station_ids[]: 54431
    station_ids[]: 54433
    station_ids[]: 54499
    station_ids[]: 54501
    station_ids[]: 54505
    station_ids[]: 54511
    station_ids[]: 54513
    station_ids[]: 54514
    station_ids[]: 54594
    station_ids[]: 54596
    station_ids[]: 54597
    select: on
    elements[]: PRS
    elements[]: PRS_Sea
    elements[]: PRS_Max
    elements[]: PRS_Min
    elements[]: WIN_S_Max
    elements[]: WIN_S_Inst_Max
    elements[]: WIN_D_INST_Max
    elements[]: WIN_D_Avg_2mi
    elements[]: WIN_S_Avg_2mi
    elements[]: WIN_D_S_Max
    elements[]: TEM
    elements[]: TEM_Max
    elements[]: TEM_Min
    elements[]: RHU
    elements[]: VAP
    elements[]: RHU_Min
    elements[]: PRE_1h
    elements[]: VIS
    elements[]: WEP_Now
    elements[]: CLO_Cov
    elements[]: CLO_COV_LM
    elements[]: CLO_Cov_Low
    elements[]: windpower
    elements[]: tigan
    isRequiredHidden[]: elements[]
    dataCode: A.0012.0001
    dataCodeInit: A.0012.0001
    show_value: normal'''
    data={}
    for x in data_str.split('\n')[1:]:
        xx=x.strip().split(': ')
        data[xx[0]]=xx[1]
    DirLogin(url,data)

