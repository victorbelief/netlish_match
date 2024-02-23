import pandas as pd
# 读取电路网表文件
with open('OTA.cir', 'r') as file:
    circuit_content = file.read()
lines = circuit_content.split('\n')  # 按行分割文本
data = []
for line in lines:
    if line.startswith(('mnm', 'mpm')):
        data.append(line.split()[:5])  # 保存前五个数据项
    elif line.startswith(('i', 'v', 'c', 'r')):
        data.append(line.split()[:3])  # 保存前三个数据项
result = {}
for item in data:
    name = item[0]
    if len(item) > 3:
        result[name + '[d]'] = item[1]
        result[name + '[g]'] = item[2]
        result[name + '[s]'] = item[3]
        result[name + '[b]'] = item[4]
    if len(item) <=3:
        result[name + '[1]'] = item[1]
        result[name + '[2]'] = item[2]
print(result)
# 构建邻接矩阵
nodes = list(result.keys())
adjacency_matrix = [[0] * len(nodes) for _ in range(len(nodes))]
mos = []
for key1, value1 in result.items():
    index1 = nodes.index(key1)  # 将键转换为整数索引
    for key2, value2 in result.items():
        index2 = nodes.index(key2)  # 将键转换为整数索引
        if value1 == value2:
            adjacency_matrix[index1][index2] = 1
            mos.append(key1)
unique_mos = list(set(mos))
print(unique_mos)
# 创建 DataFrame 对象
df = pd.DataFrame(adjacency_matrix, columns=nodes, index=nodes)
# 保存 DataFrame 到 Excel 表格
df.to_excel('adjacency_matrix.xlsx', index=True, header=True)
print(df)