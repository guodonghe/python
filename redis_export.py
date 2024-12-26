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
