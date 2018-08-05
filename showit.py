from pyecharts import Bar3D, Page, Style
from pyecharts.constants import RANGE_COLOR, WIDTH, HEIGHT
import os,datetime
import numpy
from DbCommon import mysql2pd

def create_charts():
    page = Page()
    conn=mysql2pd('140.143.161.111', '3306', 'mm', 'root', 'a091211')
    data=conn.doget("select 监测点,AQI指数,`PM2.5`,PM10,Co,No2,So2,O3,updata_time from aqi")
    conn.close()
    ps=data['监测点'].drop_duplicates().values
    ts=data['updata_time'].drop_duplicates().values
    cs=['AQI指数','PM2.5','PM10','Co','No2','So2','O3']
    for p in ps:
        res = []
        data1=data[data['监测点']==p]
        for i,c in enumerate(cs):
            for x,t in enumerate(ts):
                data2=data1[data1['updata_time']==t]
                for l in list(data2[c].values):
                    res.append([i,x,l])
        style = Style(
            width=WIDTH, height=HEIGHT
        )
        chart = Bar3D(p, **style.init_style)
        chart.add(p, ts, cs, [{'name':ts[d[1]],'value':[d[1], d[0], d[2]]} for d in res],
                  is_visualmap=True, visual_range=[0, 180],
                  visual_range_color=RANGE_COLOR,
                  grid3d_width=80, grid3d_depth=80)
        page.add(chart)
    return page
create_charts().render()
