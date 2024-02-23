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

    # 合并所有key值为一个不包含重复内容的索引列表
    merged_keys = sorted(set(key for mapping in result for key in mapping))

    return merged_keys

def read_adjacency_matrix(file_path):
    # 从excel文件中读取邻接矩阵
    df = pd.read_excel(file_path, index_col=0)
    adjacency_matrix = df.values.tolist()
    return adjacency_matrix

file_path1 = "mode_mos.xlsx"
file_path2 = "test.xlsx"
file_path3 = "adjacency_point_ota.xlsx"

adjacency_matrix1 = read_adjacency_matrix(file_path1)
adjacency_matrix2 = read_adjacency_matrix(file_path2)

adj_matrix_big = np.array(adjacency_matrix1)
adj_matrix_small = np.array(adjacency_matrix2)

df_new = pd.read_excel(file_path1, index_col=1)
merged_keys = find_subgraph_isomorphisms(adj_matrix_big, adj_matrix_small)
print(merged_keys)

# 存储所有查找到的 column_info 的列表
column_info_list = []
numeric_indices = [int(idx) for idx in merged_keys]
for idx in numeric_indices:
    try:
        column_info = df_new.iloc[idx][0]
        column_info_list.append(column_info)
        print(f"Index: {idx}, Column Info: {column_info}")
    except KeyError:
        print(f"Index: {idx} not found in the DataFrame.")
print("匹配的元器件信息:", column_info_list)

#对矩阵进行剪枝
keep_column_list = []
selected_column = []
dv = pd.read_excel(file_path3)
rows, columns = dv.shape
for keep_idx in range(rows):
    try:
        keep_column_info = dv.iloc[keep_idx][0]
        contains_element = any(element in keep_column_info for element in column_info_list)
        if contains_element:
            keep_column_list.append(keep_column_info)
            selected_column.append(keep_idx)
    except KeyError:
        print(f"Index: {keep_idx} not found in the DataFrame.")
print("保留的端口信息:", keep_column_list)
print("保留的端口索引:", selected_column)

#生成剪枝后的矩阵
first_column = dv.iloc[:, 0]
for index in range(rows):
    if index not in selected_column:
        dv = dv.drop(index, axis=0)

# 遍历并删除不在列名列表中的列
for column in dv.columns:
    if column not in keep_column_list:
        dv = dv.drop(column, axis=1)
dv.insert(0, 'port', first_column)

# 将新的矩阵保存为新的表格文件
dv.to_excel('adjacency_point_ota_cut.xlsx', index=False)