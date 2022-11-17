import requests
import random
import time
import json
import pandas as pd
import os

pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
pd.set_option("expand_frame_repr",None)
kdate="day"
ktype="sh000001"
num="10000"
def _random(n=16):
    start=10**(n-1)
    end=10**n-1
    return str(random.randint(start,end))
url=r"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_{0}qfq&param={1},{0},,,{2},qfq&r=0.{3}".format(kdate,ktype,num,_random())
def requestskline(url,max_num=5,sleep_time=random.uniform(1,5)):
    for i in range(max_num):
        headers={
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"
        }
        response=requests.get(url,headers=headers,timeout=sleep_time)
        if response.status_code==200:
            return response
        else:
            print("爬取失败",response.text)
            time.sleep(sleep_time)
content=requestskline(url).text.split("=",maxsplit=1)[-1]
content=json.loads(content)["data"][ktype]
if kdate in content:
    df=pd.DataFrame(content[kdate])
elif "qfq"+kdate in content:
    df=[pd.DataFrame(content["qfq"+kdate])]
else:
    print("已知数据不在表内")
    exit()
rename_dict={
    0:"交易日期",
    1:"开盘价",
    2:"收盘价",
    3:"最高价",
    4:"最低价",
    5:"成交量"
}
df=df.rename(columns=rename_dict)
df["交易日期"]=pd.to_datetime(df["交易日期"])
df.set_index("交易日期",inplace=True)
df["前收盘价"]=df["收盘价"].shift(1)
df["前收盘价"][0]=df["开盘价"][0]
df=df[["开盘价","最高价","最低价","收盘价","前收盘价","成交量"]]
print(df)
path=os.path.join(r"F:\stock_data\data",ktype+".csv")
df.to_csv(path)
