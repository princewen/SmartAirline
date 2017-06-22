#!/usr/bin/python
# -*- coding: utf-8 -*- ​​​​
import pandas as pd
import datetime
import numpy as np


df = pd.read_csv('../data/t2.csv',encoding='gbk',index_col=None)
print (df)


def get_time_range():
    """得到起飞时间的最小值，和到达时间的最大值，作为时间范围"""
    minTime = df['起飞时间'].min()
    maxTime = df['到达时间'].max()
    """字符串转时间"""
    min_datetime = datetime.datetime.strptime(minTime, "%Y/%m/%d %H:%M")
    max_datetime = datetime.datetime.strptime(maxTime,"%Y/%m/%d %H:%M")
    """计算两个时间的差值"""
    minutes = int(((max_datetime-min_datetime).seconds)/60)+(max_datetime-min_datetime).days*1440
    timelist = []
    for i in range(1,minutes+2):
        timelist.append((min_datetime+datetime.timedelta(minutes=(i-1)),i))
    time_df = pd.DataFrame(timelist,columns=['起飞时间','起飞时间id'])
    time_df.to_csv('../data/time.csv',encoding='gbk')


def merge_time():
    """得到xjt矩阵"""
    time_df = pd.read_csv('../data/time.csv',encoding='gbk',index_col=0)
    time_list = time_df['起飞时间id'].values.tolist()
    print (time_list)
    air_list = df['航班ID'].values.tolist()
    """创建一个全0的ndarray，然后首列用于保存航班ID"""
    time_np = np.zeros((len(air_list),len(time_list)+1))

    """找到每一个航班的起飞时间对应的列，同时对应的位置赋值为1"""
    for value in air_list:
        time_np[value-1,0] = value
        date_index = time_df[time_df['起飞时间']==df[df['航班ID']==value]['起飞时间'].values[0]]['起飞时间id']
        time_np[value-1,date_index] = 1
    """将ndarray变为dataframe ，同时写入csv"""
    merge_df = pd.DataFrame(time_np,index=air_list,columns=['航班ID']+time_list)
    merge_df.to_csv('../data/xit.csv',encoding='gbk')




def process_t2():
    """
    处理tbale2
    :return: 
    """
    """处理原字符串，转换为%Y-%m-%d %H:%M:%S格式"""
    for i in range(len(df.index)):
        start_time = df.ix[i,'起飞时间']
        start_datetime = datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M")
        df.ix[i,'起飞时间'] = str(start_datetime)

        end_time = df.ix[i, '到达时间']
        end_datetime = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M")
        df.ix[i, '到达时间'] = str(end_datetime)

    """增加对应航班一列"""
    df['对应航班'] = [None] * len(df.index)

    """按照航班号进行分组，处理拉直情况"""
    group_df = df.groupby(['航班号'])
    for (id,data) in group_df:
        """如果同一航班对应多个航班ID，则存在拉直情况"""
        if len(data.index) > 1:
            data.index = range(len(data.index))
            print (data.ix[0,'日期'])
            new_data = [len(df.index)+1,data.ix[0,'日期'],data.ix[0,'国际/国内'],data.ix[0,'航班号'],
                        data.ix[0,'起飞机场'],data.ix[len(data.index)-1,'到达机场']]
            minute_delta = 0
            union_id = []
            """计算所有航班飞行的总时间，以计算拉直到达时间，同时添加关联的航班ID"""
            for t in range(len(data.index)):
                start_time = data.ix[t, '起飞时间']
                start_datetime = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                end_time = data.ix[t, '到达时间']
                end_datetime = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                minute_delta += int(((end_datetime - start_datetime).seconds) / 60) + (end_datetime - start_datetime).days * 1440
                union_id.append(str(data.ix[t,'航班ID']))

            """计算到达时间"""
            start_time = data.ix[0,'起飞时间']
            start_datetime = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime+datetime.timedelta(minutes=minute_delta)
            new_data += [str(start_datetime),str(end_datetime),data.ix[0,'飞机ID'],data.ix[0,'机型'],data.ix[0,'重要系数'],'|'.join(union_id)]
            """将新数据添加到最后一行"""
            df.loc[len(df.index)] = new_data

    """写入新的文件"""
    print (df)
    df.to_csv('../data/t2_new.csv',encoding='gbk')



def main():
    process_t2()
    get_time_range()
    merge_time()


if __name__ == '__main__':
    main()