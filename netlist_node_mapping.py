import pandas as pd

def netlist_node_mapping_mos(netlist_path, adjacency_matrix_path):
    # 读取电路网表文件
    with open(netlist_path, 'r') as file:
        circuit_content = file.read()
    lines = circuit_content.split('\n')  # 按行分割文本
    data = []
    for line in lines:
        if line.startswith(('mnm', 'mpm')):
            data.append(line.split()[:5])  # 保存前五个数据项
        elif line.startswith(('i', 'v', 'c', 'r')):
            data.append(line.split()[:3])  # 保存前三个数据项

    # 将mos管等效为一个节点
    result_mos = {item[0]: item[1:] for item in data}
    nodes = list(result_mos.keys())
    adjacency_matrix_mos = [[0] * len(nodes) for _ in range(len(nodes))]
    for key1, value1 in result_mos.items():
        index1 = nodes.index(key1)  # 将键转换为整数索引
        for key2, value2 in result_mos.items():
            index2 = nodes.index(key2)  # 将键转换为整数索引
            if set(value1) & set(value2):
                adjacency_matrix_mos[index1][index2] = 1
    # 创建 DataFrame 对象
    df = pd.DataFrame(adjacency_matrix_mos, columns=nodes, index=nodes)
    # 保存 DataFrame 到 Excel 表格
    df.to_excel(adjacency_matrix_path, index=True, header=True)
    return df.to_excel

def netlist_node_mapping_point(netlist_path, adjacency_matrix_path):
    # 读取电路网表文件
    with open(netlist_path, 'r') as file:
        circuit_content = file.read()
    lines = circuit_content.split('\n')  # 按行分割文本
    data = []
    for line in lines:
        if line.startswith(('mnm', 'mpm')):
            data.append(line.split()[:5])  # 保存前五个数据项
        elif line.startswith(('i', 'v', 'c', 'r')):
            data.append(line.split()[:3])  # 保存前三个数据项
    # 保存端点信息
    result_point= {}
    for item in data:
        name = item[0]
        if len(item) > 3:
            result_point[name + '[d]'] = item[1]
            result_point[name + '[g]'] = item[2]
            result_point[name + '[s]'] = item[3]
            result_point[name + '[b]'] = item[4]
        if len(item) <=3:
            result_point[name + '[1]'] = item[1]
            result_point[name + '[2]'] = item[2]
    # 构建邻接矩阵
    nodes = list(result_point.keys())
    adjacency_matrix_point = [[0] * len(nodes) for _ in range(len(nodes))]
    for key1, value1 in result_point.items():
        index1 = nodes.index(key1)  # 将键转换为整数索引
        for key2, value2 in result_point.items():
            index2 = nodes.index(key2)  # 将键转换为整数索引
            if value1 == value2:
                adjacency_matrix_point[index1][index2] = 1
    # 创建 DataFrame 对象
    df = pd.DataFrame(adjacency_matrix_point, columns=nodes, index=nodes)
    # 保存 DataFrame 到 Excel 表格
    df.to_excel(adjacency_matrix_path, index=True, header=True)
    return df.to_excel
