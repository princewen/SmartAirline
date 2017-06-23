import pandas as pd
import numpy as np


df = pd.read_csv('../data/t2_new.csv',index_col=0,encoding='gbk')

def create_B_table():
    line_len = len(list(set(df['航班ID'].values.tolist())))
    plane_len = len(list(set(df['飞机ID'].values.tolist())))
    b_np = np.zeros((line_len,plane_len),dtype=np.int32)
    for i in df.index:
        line_id = df.ix[i,'航班ID']
        plane_id = df.ix[i,'飞机ID']
        b_np[line_id-1,plane_id-1] = 1
    b_df = pd.DataFrame(b_np,index=range(1,line_len+1),columns=range(1,plane_len+1))
    b_df.to_csv('../data/bij.csv',encoding='gbk')

def main():
    create_B_table()


if __name__ == '__main__':
    main()