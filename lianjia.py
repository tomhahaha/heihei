# 导入开发模块
import requests
from bs4 import BeautifulSoup

# 定义空列表，用于创建所有的爬虫链接
urls = []
# 指定爬虫所需的上海各个区域名称
citys = ['dongcheng','xicheng','chaoyang','haidian','fengtai','shijingshan','tongzhou','changping',
         'yizhuangkaifaqu','shunyi','fangshan','mentougou','pinggu','huairou','miyun']

# 基于for循环，构造完整的爬虫链接
for i in citys:
    url = 'https://bj.lianjia.com/ershoufang/%s/' %i
    res = requests.get(url) # 发送get请求
    res = res.text.encode(res.encoding).decode('utf-8') # 需要转码，否则会有问题
    soup = BeautifulSoup(res,'html.parser') # 使用bs4模块，对响应的链接源代码进行html解析
    page = soup.findAll('div',{'class':'page-box house-lst-page-box'}) # 使用finalAll方法，获取指定标签和属性下的内容
#    pages = [i.strip() for i in page[0].text.split('\n')] # 抓取出每个区域的二手房链接中所有的页数
    if not len(page)==0:
#    if len(pages) > 3:
#        total_pages = int(pages[-3])
#    else:
#        total_pages = int(pages[-2])
        total_pages=int((str)(page[0]).split('"totalPage":')[1].split(',"curPage"')[0])
        for j in list(range(1,total_pages+1)): # 拼接所有需要爬虫的链接
            urls.append('https://bj.lianjia.com/ershoufang/%s/pg%s' %(i,j))
print('urls collect finish！')
# 创建csv文件，用于后面的保存数据
file = open('lianjia.csv','w',encoding = 'utf-8')
for url in urls: # 基于for循环，抓取出所有满足条件的标签和属性列表，存放在find_all中
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    find_all = soup.find_all(name = 'div', attrs = {'class':'info clear'})
    print(url)
    for i in list(range(len(find_all))): # 基于for循环，抓取出所需的各个字段信息
        res2 = find_all[i]
        title = res2.find_all('div', {'class': 'title'})[0].find_all('a')[0].text  # 每套二手房的标语
        houseInfo=res2.find_all('div',{'class':'houseInfo'})[0]
        name =houseInfo.find_all('a')[0].text # 每套二手房的小区名称
        room_type =houseInfo.text.split('|')[1] # 每套二手房的户型
        size =houseInfo.text.split('|')[2].strip()  # 每套二手房的面积
        chaoxiang =houseInfo.text.split('|')[3].strip()  # 每套二手房的朝向
        positionInfo=res2.find_all('div', {'class': 'positionInfo'})[0]
        if positionInfo.text.find(')')==-1:
            if positionInfo.text.find('层') == -1:
                loucheng ='-1'  # 每套二手房所在的楼层
                builtdate = positionInfo.text.split('年')[0].strip()  # 每套二手房的建筑时间
            else:
                loucheng = positionInfo.text.split('层')[0].strip() + '层'  # 每套二手房所在的楼层
                builtdate = positionInfo.text.split('层')[1].split('年')[0].strip()  # 每套二手房的建筑时间
        else:
            loucheng = positionInfo.text.split(')')[0].strip()+')' # 每套二手房所在的楼层
            builtdate =positionInfo.text.split(')')[1].split('年')[0].strip() # 每套二手房的建筑时间
        region =positionInfo.find_all('a')[0].text # 每套二手房所属的区域
		# 每套二手房的总价
        price = find_all[i].find('div',{'class':'totalPrice'}).find_all('span')[0].text
		# 每套二手房的平方米售价
        price_union = find_all[i].find('div',{'class':'unitPrice'}).find_all('span')[0].text

        #print(name,room_type,size,region,loucheng,chaoxiang,price,price_union,builtdate)
		# 将上面的各字段信息值写入并保存到csv文件中
        file.write(','.join((name,room_type,size,region,loucheng,chaoxiang,price,price_union,builtdate))+'\n')
# 关闭文件（否则数据不会写入到csv文件中）
print('finished！')
file.close()