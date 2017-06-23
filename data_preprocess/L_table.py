import pandas as pd
import datetime
import numpy as np

df = pd.read_csv('../data/t2_new.csv',index_col=0,encoding='gbk')
t3_df = pd.read_csv('../data/t3.csv',index_col =None,encoding='gbk')
airport_df = pd.read_csv('../data/airport_id.csv',index_col =0,encoding='gbk')

def get_all_plane_id():
    plane_id = df['飞机ID'].values.tolist()
    plane_id = list(set(plane_id))
    return plane_id



def create_L_table():
    plane_id = get_all_plane_id()
    plane_len = len(plane_id)
    airport_len = len(airport_df['机场'])
    jkk_np = np.zeros((plane_len,airport_len,airport_len),dtype=np.int32)
    for i in plane_id:

        sub_df = t3_df[t3_df['限制飞机']==i]
        print (sub_df)
        for t in sub_df.index:
            start_airport = sub_df.ix[t,'起飞机场']
            end_airport = sub_df.ix[t,'到达机场']
            start_airport_id = airport_df[airport_df['机场']==start_airport]['机场id']
            end_airport_id = airport_df[airport_df['机场']==end_airport]['机场id']
            jkk_np[i-1,start_airport_id-1,end_airport_id-1] = 1

    index1 = []
    for t in range(1,plane_len+1):
        index1 += [t] * airport_len

    index2 = airport_df['机场id'].values.tolist() * plane_len
    index = pd.MultiIndex.from_arrays([index1,index2],names=['飞机ID','起飞机场ID'])
    jkk_np=jkk_np.reshape(-1,airport_len)
    jkk_df = pd.DataFrame(jkk_np,index = index,columns=airport_df['机场id'].values.tolist())
    jkk_df.to_csv('../data/jkk.csv', encoding='gbk')






def main():
    create_L_table()


if __name__ == '__main__':
    main()