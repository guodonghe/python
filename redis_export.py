import redis

# 连接 Redis
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# 获取键值
key = "C2:common:b_token"
value = r.get(key)

# 保存到文件
if value:
    with open("output.txt", "w") as f:
        f.write(value)
    print(f"Value of '{key}' has been exported to output.txt")
else:
    print(f"Key '{key}' does not exist.")


# redis key 如果是列表类型

# -*- coding: utf-8 -*-
import redis

# 连接 Redis
r = redis.StrictRedis(host='ulu-redis-api-mq.inthd.xyz', port=6379,password='N8YtgU', decode_responses=True)

# 获取键值
key = "huidian:statistic:face_enter"


# 检查键是否存在
if r.exists(key):
    # 检查键类型
    key_type = r.type(key)
    if key_type == "list":
        # 使用 lrange 获取列表所有元素
        values = r.lrange(key, 0, -1)  # 获取整个列表
        # 将结果保存到文件
        with open("output.txt", "w") as f:
            f.writelines(value + "\n" for value in values)
        print(f"List values of '{key}' have been exported to output.txt")
    else:
        print(f"Key '{key}' is not a list. It is of type '{key_type}'.")
else:
    print(f"Key '{key}' does not exist.")
