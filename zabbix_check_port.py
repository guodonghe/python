import sys
import http.client

def check_http_service(addr, port, check_url):
    """
    检查 HTTP 服务是否可用并返回状态码
    """
    try:
        # 建立 HTTP 连接
        conn = http.client.HTTPConnection(addr, port, timeout=10)
        conn.request("GET", check_url)
        response = conn.getresponse()
        return response.status
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python check_http.py <address> <port> <url>")
        sys.exit(1)

    # 从命令行获取参数
    addr = sys.argv[1]
    port = int(sys.argv[2])
    check_url = sys.argv[3]

    # 调用检查服务的函数
    result = check_http_service(addr, port, check_url)

    # 根据返回结果打印详细信息
    if isinstance(result, int):
        if result == 200:
            print(f"Service is OK. HTTP Status: {result}")
        elif result == 404:
            print(f"Service not found. HTTP Status: {result}")
        else:
            print(f"Service returned status code: {result}")
    else:
        print(result)

# 使用示例
python http_check.py 172.30.70.200 8002 /api/v1/tasks/2/
# 修改zabbix配置文件
UserParameter=check.http.service[*],python /path/to/check_http.py $1 $2 $3
# 验证 Zabbix 配置
zabbix_agentd -t "check.http.service[127.0.0.1,80,/]"
# 创建触发器
{Template Name:check.http.service[{HOST.IP},80,/].str(ERROR)}=1



