from itertools import combinations
import networkx as nx
import pandas as pd

def adjacency_matrix_to_graph_from_excel(file_path):
    # 从 Excel 文件读取邻接矩阵和结点的标题信息
    df = pd.read_excel(file_path, index_col=0)
    adjacency_matrix = df.values.tolist()
    node_labels = df.columns.tolist()

    # 创建一个空的图
    graph = nx.Graph()

    # 添加结点，内容为矩阵标题的形式
    for label in node_labels:
        graph.add_node(label)

    # 获取邻接矩阵的大小
    num_nodes = len(adjacency_matrix)

    # 遍历邻接矩阵
    for i in range(num_nodes):
        for j in range(num_nodes):
            # 如果是对角线元素，表示结点自身，则跳过
            if i == j:
                continue
            # 如果邻接矩阵的值为1，则表示结点i和j之间存在连接关系
            if adjacency_matrix[i][j] == 1:
                # 在图中添加对应的边
                graph.add_edge(node_labels[i], node_labels[j])

    return graph

# 检查结点开头的字符是否满足条件
def count_nodes_with_prefix(graph, prefix):
    count = 0
    for node in graph.nodes():
        if node.startswith(prefix):
            count += 1
    return count

# 检查结点的第二个字符是否满足条件
def count_nodes_with_second_char(graph, char):
    count = 0
    for node in graph.nodes():
        if len(node) >= 2 and node[1] == char:
            count += 1
    return count

def find_subgraphs_with_conditions(graph, num_nodes, num_edges, p_mos_2, n_mos_2, v_count_2, i_count_2, c_count_2, r_count_2):
    all_subgraphs = []

    # 生成和匹配目标相同数量的结点组合
    node_combinations = combinations(graph.nodes(), num_nodes)
    # 遍历每个结点组合，检查是否能构成子图
    for nodes in node_combinations:
        subgraph = graph.subgraph(nodes)
        # 如果子图的结点数等于给定数量，则检查边数是否符合要求
        if subgraph.number_of_nodes() == num_nodes and subgraph.number_of_edges() == num_edges:
            # 如果边数也符合要求，则检查每个元器件数量是否符合要求
            p_mos_1 = count_nodes_with_second_char(subgraph, "p");
            n_mos_1 = count_nodes_with_second_char(subgraph, "n");
            v_count_1 = count_nodes_with_prefix(subgraph, "v");
            i_count_1 = count_nodes_with_prefix(subgraph, "i");
            c_count_1 = count_nodes_with_prefix(subgraph, "c");
            r_count_1 = count_nodes_with_prefix(subgraph, "r");
            # 如果满足所有条件，则将子图添加到结果中
            if (p_mos_1 == p_mos_2 and n_mos_1 == n_mos_2 and v_count_1 == v_count_2 and i_count_1 == i_count_2
            and c_count_1 == c_count_2 and r_count_1 == r_count_2):
                all_subgraphs.append(subgraph)

    return all_subgraphs

# 待匹配电路的矩阵文件路径
file_path1 = "adjacency_mos_ota_two.xlsx"
# 目标电路的矩阵文件路径
file_path2 = "adjacency_mos_ota.xlsx"

# 将邻接矩阵转换为图，并使用 Excel 文件中的标题作为结点值
graph1 = adjacency_matrix_to_graph_from_excel(file_path1)
graph2 = adjacency_matrix_to_graph_from_excel(file_path2)

# 计算目标电路各个元器件的数量
p_mos_2 = count_nodes_with_second_char(graph2, "p");
n_mos_2 = count_nodes_with_second_char(graph2, "n");
v_count_2 = count_nodes_with_prefix(graph2, "v");
i_count_2 = count_nodes_with_prefix(graph2, "i");
c_count_2 = count_nodes_with_prefix(graph2, "c");
r_count_2 = count_nodes_with_prefix(graph2, "r");

# 执行匹配
matching_subgraphs = find_subgraphs_with_conditions(graph1, len(graph2.nodes), len(graph2.edges),
p_mos_2, n_mos_2, v_count_2, i_count_2, c_count_2, r_count_2)

# 输出两个图的结点和边
print("结点:", graph1.nodes())
print("边:", graph1.edges())
print("结点:", graph2.nodes())
print("边:", graph2.edges())
# 输出匹配结果
for subgraph in matching_subgraphs:
    print("匹配的电路结构:")
    print("结点:", subgraph.nodes())
    print("边:", subgraph.edges())

