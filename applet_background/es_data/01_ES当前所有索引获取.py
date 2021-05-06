from es_data.es_conf import es_con


# 方法1
indices = es_con.indices.get_alias("*")
# print(indices)

# 方法2
# 使用通配符。
indices = es_con.indices.get('*')
# for index in indices:
#     print(index)
# print(indices)

# 方法3
# 直接获取索引列表
indices = sorted(es_con.indices.get_alias().keys())
print(indices)