from itertools import combinations
import networkx as nx
import numpy as np
import pandas as pd

def adjacency_matrix_to_graph(adj_matrix):
    # 创建一个空图
    graph = nx.Graph()

    # 获取邻接矩阵的大小
    num_nodes = len(adj_matrix)

    # 遍历邻接矩阵
    for i in range(num_nodes):
        for j in range(num_nodes):
            # 如果是对角线元素，跳过
            if i == j:
                continue
            # 如果邻接矩阵的值为1，则表示节点i和节点j之间存在连接
            if adj_matrix[i][j] == 1:
                # 在图中添加对应的边
                graph.add_edge(i, j)

    return graph

def read_adjacency_matrix(file_path):
    # 从Excel文件中读取邻接矩阵
    df = pd.read_excel(file_path, index_col=0)
    adjacency_matrix = df.values.tolist()
    return adjacency_matrix

def find_subgraphs(graph, num_nodes, num_edges):
    all_subgraphs = []

    # 生成特定数量的节点组合
    node_combinations = combinations(graph.nodes(), num_nodes)
    # 遍历每个节点组合，检查是否为子图
    for nodes in node_combinations:
        subgraph = graph.subgraph(nodes)
        # 如果子图的节点数等于给定数量，则检查边数是否符合要求
        if subgraph.number_of_nodes() == num_nodes and subgraph.number_of_edges() == num_edges:
            all_subgraphs.append(subgraph)

    return all_subgraphs

file_path1 = "adjacency_mos_ota_two.xlsx"
file_path2 = "adjacency_mos_ota.xlsx"

adjacency_matrix1 = read_adjacency_matrix(file_path1)
adjacency_matrix2 = read_adjacency_matrix(file_path2)

# 将邻接矩阵转换为图
graph1 = adjacency_matrix_to_graph(adjacency_matrix1)
graph2 = adjacency_matrix_to_graph(adjacency_matrix2)
matching_subgraphs = find_subgraphs(graph1, len(graph2.nodes), len(graph2.edges))

print(len(graph1.nodes),graph1.nodes)
print(len(graph1.edges),graph1.edges)
print(len(graph2.nodes),graph2.nodes)
print(len(graph2.edges),graph2.edges)
print(matching_subgraphs)

# 打印图的节点和边
for subgraph in matching_subgraphs:
    print("匹配的电路结构:")
    print("结点:", subgraph.nodes)
    print("边:", subgraph.edges)

