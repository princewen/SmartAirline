
#!/usr/bin/python
# -*- coding: utf-8 -*- ​​​​
import pandas as pd
import datetime
import numpy as np


df = pd.read_csv('../data/t2.csv',encoding='gbk',index_col=None)
print (df)
def processG1():
    """读取最大的ID和机型，用于初始化"""
    maxAirID = df['飞机ID'].max()
    maxAirtype = df['机型'].max()
    print(maxAirtype,maxAirID)
    airplaneId = df['飞机ID'].values.tolist()
    airlinetype = df['机型'].values.tolist()
    G1 = np.zeros((maxAirID,maxAirtype))
    """飞机ID与其对应的机型处标1"""
    for i in range(len(df.index)):
        G1[airplaneId[i]-1][airlinetype[i]-1] = 1
    G1list = pd.DataFrame(G1,index=range(1,maxAirID+1),columns=range(1,maxAirtype+1))
    G1list.to_csv('../data/G1.csv',encoding='gbk')

def processG2():
    """读取最大的航班ID和机型，用作初始化"""
    maxFlight = df['航班ID'].max()
    maxAirtype = df['机型'].max()
    FlightId = df['航班ID'].values.tolist()
    airlinetype = df['机型'].values.tolist()
    G2=np.zeros((maxFlight,maxAirtype))
    """航班ID与其对应的机型处标1"""
    for i in range(len(df.index)):
        G2[FlightId[i]-1][airlinetype[i]-1] = 1
    G2list = pd.DataFrame(G2,index=range(1,maxFlight+1),columns=range(1,maxAirtype+1))
    G2list.to_csv('../data/G2.csv', encoding='gbk')

def main():
    processG1()
    processG2()
if __name__ == '__main__':
    main()