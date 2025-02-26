import numpy as np
import pandas as pd
import umap     # 使用 UMAP 将数据降维到二维
from kmeans_pytorch import kmeans as KMeans
import matplotlib.pyplot as plt
import torch
import os

def one_hot_encode(data) :        #独热编码操作函数
    bases = ['a' , 'c' , 'g' , 't']
    base_dict = dict(zip(bases,range(4))) # {'A' : 0, 'C' : 1, 'G' : 2, 'T' : 3}
    
    n = len(data)
    total_width = data.str.len().max()
    X = np.zeros((n, 4, total_width))

    seqs = data.values
    
    for i in range(n):
        seq = seqs[i]
        # loop through each individual sequence, from the 5' to 3' end
        for b in range(len(seq)):
            # this will assign a 1 to the appropriate base and position for this UTR sequence
            X[i, base_dict[seq[b]], b + 96 - len(seq)] = 1.

    return X

import time

def kmeans(data_path,preprocessed_data_dir):    #Kmeans聚类，随机选出来一部分数据UMP降维给用户看，聚类是对所有数据聚类
    x_umap = np.load('storage/preprocessed_data/working_set/x_umap.npy')  # !!!调试时使用
    cluster_ids_x = np.load('storage/preprocessed_data/working_set/cluster_ids_x.npy')  # !!!调试时使用
    Protein = np.load('storage/preprocessed_data/working_set/Protein.npy')  # !!!调试时使用
    # x = np.load('storage/preprocessed_data/working_set/x.npy')  # !!!调试时使用
    # n_clusters = 56
    # device=torch.device('cuda:0')
    # x_tensor = torch.tensor(x.reshape(x.shape[0],-1), dtype=torch.float32).to(device)
    # cluster_ids_x, cluster_centers = KMeans(x_tensor,num_clusters=n_clusters,device=device)
    time.sleep(3)
    return x_umap , Protein , cluster_ids_x  # !!!调试时使用
    
    #使用pandas读取数据集，.dropna()用于删除数据集中缺失值的行，reset_index(drop= True)用于重置索引
    raw_data = pd.read_csv(data_path).dropna().reset_index(drop= True)
    x = raw_data['Sequence']
    Protein = raw_data['Protein'].to_numpy()
    x = one_hot_encode(x)   # 独热编码
    
    # 生成随机索引，以随机选择数据（选出来UMP降维给用户看的，聚类是对所有数据聚类）
    select_data_size = 10000     # 从原始数据集中随机选择select_data_size个数据 展示给用户
    random_indices = np.random.choice(x.shape[0], size=select_data_size, replace=False)
    # 使用随机索引从数据集中选择数据
    x_selected = x[random_indices]
    Protein_selected = Protein[random_indices]
    # 使用 UMAP 将数据降维到二维（非常耗时）
    x_umap = umap.UMAP(
        densmap=True,
        n_neighbors=15,
        min_dist=0,
        n_components=2,
        low_memory=True,
    ).fit(x_selected.reshape(select_data_size,-1))
    x_umap = x_umap.embedding_
    
    # 转为tensor

    # KMeans 聚类
    # 【Bug】数据量太大根本跑不动：[enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 17572896768 bytes.
    # 明明我已经用了GPU了它还是用CPU给我跑
    n_clusters = 56
    device=torch.device('cuda:0')
    x_tensor = torch.tensor(x.reshape(x.shape[0],-1), dtype=torch.float32).to(device)
    cluster_ids_x, cluster_centers = KMeans(x_tensor,num_clusters=n_clusters,device=device)
        
     # 以numpy格式保存: x, Protein, cluster_ids_x （保存在同名文件夹下）
    filename = os.path.splitext(os.path.basename(data_path))[0]
    dir = os.path.join(preprocessed_data_dir, filename)
    os.makedirs(dir, exist_ok=True)
    np.save(os.path.join(dir, 'x.npy'), x)
    np.save(os.path.join(dir, 'Protein.npy'), Protein)
    np.save(os.path.join(dir, 'cluster_ids_x.npy'), cluster_ids_x)
    np.save(os.path.join(dir, 'x_umap.npy'), x_umap)
    
    
    return x_umap , Protein_selected , cluster_ids_x[random_indices]


if __name__ == '__main__':
    raw_data_path = r'storage\original_data\working_set.csv'
    original_data_dir = 'storage/original_data/'
    preprocessed_data_dir = 'storage/preprocessed_data/'
    kmeans(raw_data_path,preprocessed_data_dir)