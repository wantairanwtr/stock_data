import requests
import pandas as pd
import time
import re
import json
import os
import random

pd.set_option("display.max_row",None)
pd.set_option("display.max_columns",None)
pd.set_option("expand_frame_repr",False)

def requestsurl(url,max_num=5,sleep_time=5):
    headers={"user-agent":r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42",
             "referer":r"https://vip.stock.finance.sina.com.cn/mkt/"}
    for i in range(max_num):
        response=requests.get(url,headers=headers,timeout=sleep_time)
        if response.status_code==200:
            return response
        else:
            print("爬取失败",response)
            time.sleep(sleep_time)
def getDate():
    url = 'https://hq.sinajs.cn/list=sh000001'
    response = requestsurl(url).text
    data_date = str(response.split(',')[-4])
    # 获取上证的指数日期
    return data_date

def getStockdata():
    all_data=pd.DataFrame()
    page=1
    while True:
        url=r"https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={}&num=80&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=sort".format(page)
        content=requestsurl(url).text
        if content=="[]":
            print("爬取完成")
            break
        print("正在爬取第{}页".format(page))
        content=json.loads(content)
        df=pd.DataFrame(content,dtype=float)
        all_data=all_data.append(df,ignore_index=True)
        page+=1
        time.sleep(random.uniform(0,3))
    rename_dict={
        'symbol': '股票代码', 'code': '交易日期', 'name': '股票名称', 'open': '开盘价',
        'settlement': '前收盘价', 'trade': '收盘价', 'high': '最高价', 'low': '最低价',
        'buy': '买一', 'sell': '卖一', 'volume': '成交量', 'amount': '成交额',
        'changepercent': '涨跌幅', 'pricechange': '涨跌额',
        'mktcap': '总市值', 'nmc': '流通市值', 'ticktime': '数据更新时间', 'per': 'per', 'pb': '市净率',
        'turnoverratio': '换手率'
    }
    all_data.rename(columns=rename_dict,inplace=True)
    all_data["交易日期"]=pd.to_datetime(getDate())
    all_data["总市值"]*=10000
    all_data["流通市值"]*=10000
    all_data=all_data[['股票代码', '股票名称', '交易日期', '开盘价', '最高价', '最低价', '收盘价', '前收盘价', '成交量', '成交额', '流通市值', '总市值']]
    return all_data

all_data=getStockdata()
all_data=all_data[all_data["开盘价"]-0>0.00001]
all_data.reset_index(drop=True,inplace=True)

dir=r"F:\stock_data\data\stock"
if not os.path.exists(dir):
    os.mkdir(dir)

for i in all_data.index:
    d=all_data.loc[i:i]
    name=d["股票代码"][i]
    path=os.path.join(dir,name+".csv")
    if os.path.exists(path):
        d.to_csv(path,mode="a",encoding="gbk",header=False,index=False)
    else:
        pd.DataFrame(columns=["此数据由微博quantoken整理,微信:quant689"]).to_csv(path,mode="w",encoding="gbk",header=True,index=False)
        d.to_csv(path,encoding="gbk",mode="a",header=True, index=False)
    print(name)
