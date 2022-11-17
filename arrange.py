import os
import pandas as pd
path=r"F:\zuoye\data\stock"
ls=[]
for root,dirs,files in os.walk(path):
    for i in files:
        ls.append(i)
for i in ls:
    file=os.path.join(path,i)
    df=pd.read_csv(file,skiprows=1,encoding="gbk")
    pd.DataFrame(columns=["此数据由微博quantoken整理,微信:quant689"]).to_csv(file,mode="w",header=True,encoding="gbk",index=False)
    df.to_csv(file,mode="a",header=True,encoding="gbk",index=False)
    print(file)