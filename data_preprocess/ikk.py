import pandas as pd
import numpy as np

df = pd.read_csv('../data/t2_new.csv',index_col=0,encoding='gbk')
t3_df = pd.read_csv('../data/t3.csv',index_col =None,encoding='gbk')


def get_all_airport():
    """得到所有的机场列表，并写入一个csv"""
    start_airport = df['起飞机场'].values.tolist()
    end_airport = df['到达机场'].values.tolist()
    """利用set不允许有重复元素的特性"""
    airports = list(set(start_airport + end_airport))
    start_airport = t3_df['起飞机场'].values.tolist()
    end_airport = t3_df['到达机场'].values.tolist()
    airports = list(set(airports+start_airport + end_airport))
    print (airports)
    ids = range(1,len(airports)+1)
    """写入文件"""
    airport_df = pd.DataFrame(list(zip(airports,ids)),columns=['机场','机场id'])
    airport_df.to_csv('../data/airport_id.csv',encoding='gbk')

def create_ikk():
    """得到ikk矩阵"""
    airport_df = pd.read_csv('../data/airport_id.csv',encoding='gbk',index_col=0)
    """将两个表合并，得到起飞机场和到达机场的id"""
    airport_df.columns=['起飞机场','起飞机场id']
    merge_df = pd.merge(df,airport_df,how='left')
    airport_df.columns=['到达机场','到达机场id']
    merge_df = pd.merge(merge_df,airport_df,how='left')
    """创建一个np数组，形状为（i，k，k）"""
    ikk_np = np.zeros((len(merge_df['航班ID'].values.tolist()),len(airport_df['到达机场'].values.tolist()),len(airport_df['到达机场'].values.tolist())),dtype=np.int32)
    print(ikk_np.shape)
    for i in merge_df.index:
        x = int(merge_df.ix[i,'起飞机场id'])
        y = int(merge_df.ix[i,'到达机场id'])
        ikk_np[i,x-1,y-1] = 1

    """由于不能将三维数组传给DataFrame，所以使用层次化索引，每一个航班id对应k行"""
    index1 = []
    for i in range(1,len(merge_df['航班ID'].values.tolist())+1):
        index1 = index1 + [i] * (len(airport_df['到达机场'].values.tolist()))
    """机场id重复i次"""
    index2 = airport_df['到达机场id'].values.tolist() * len(merge_df['航班ID'].values.tolist())
    #print (ikk_np)
    ikk_np = ikk_np.reshape(-1,len(airport_df['到达机场'].values.tolist()))
    """构建层次化索引"""
    index = pd.MultiIndex.from_arrays([index1,index2],names=['航班ID',"起飞机场ID"])
    """创建dataframe并写入文件"""
    ikk_df = pd.DataFrame(ikk_np,index=index,columns=airport_df['到达机场id'].values.tolist())
    print (ikk_df)
    ikk_df.to_csv('../data/ikk.csv',encoding='gbk')
    #print (ikk_df)



def main():
    get_all_airport()
    #test_index()
    create_ikk()

if __name__ == '__main__':
    main()