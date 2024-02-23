import networkx as nx
import numpy as np
import pandas as pd

def find_subgraph_isomorphisms(adj_matrix_big, adj_matrix_small):
    big_graph = nx.Graph(adj_matrix_big)
    small_graph = nx.Graph(adj_matrix_small)

    result = []

    vf2 = nx.algorithms.isomorphism.GraphMatcher(big_graph, small_graph)

    for subgraph in vf2.subgraph_isomorphisms_iter():
        simplified_mapping = tuple(sorted(str(key) for key in subgraph.keys()))
        result.append(simplified_mapping)

    # 使用排序后的元组进行去重
    result = list(set(result))

    # 合并所有键的结果为一个不包含重复内容的索引列表
    merged_keys = sorted(set(key for mapping in result for key in mapping))

    return merged_keys

def read_adjacency_matrix(file_path):
    # 从Excel文件中读取邻接矩阵
    df = pd.read_excel(file_path, index_col=0)
    adjacency_matrix = df.values.tolist()
    return adjacency_matrix

file_path1 = "mode_mos.xlsx"
file_path2 = "test.xlsx"

adjacency_matrix1 = read_adjacency_matrix(file_path1)
adjacency_matrix2 = read_adjacency_matrix(file_path2)

# 使用示例
adj_matrix_big = np.array(adjacency_matrix1)
adj_matrix_small = np.array(adjacency_matrix2)

df = pd.read_excel(file_path1, index_col=1)

merged_keys = find_subgraph_isomorphisms(adj_matrix_big, adj_matrix_small)
print(merged_keys)

# 存储所有查找到的 column_info 的列表
column_info_list = []
numeric_indices = [int(idx) for idx in merged_keys]
for idx in numeric_indices:
    try:
        column_info = df.iloc[idx][0]
        column_info_list.append(column_info)
        print(f"Index: {idx}, Column Info: {column_info}")
    except KeyError:
        print(f"Index: {idx} not found in the DataFrame.")
print("匹配的元器件信息:", column_info_list)