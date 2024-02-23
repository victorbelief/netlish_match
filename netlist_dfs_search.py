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
    return result

def read_adjacency_matrix(file_path):
    # 从Excel文件中读取邻接矩阵
    df = pd.read_excel(file_path, index_col=0)
    adjacency_matrix = df.values.tolist()
    return adjacency_matrix

file_path1 = "adjacency_mos_ota_two.xlsx"
file_path2 = "adjacency_mos_ota.xlsx"

adjacency_matrix1 = read_adjacency_matrix(file_path1)
adjacency_matrix2 = read_adjacency_matrix(file_path2)

# 使用示例
adj_matrix_big = np.array(adjacency_matrix1)
adj_matrix_small = np.array(adjacency_matrix2)

isomorphisms = find_subgraph_isomorphisms(adj_matrix_big, adj_matrix_small)
for mapping in isomorphisms:
    print(mapping)










