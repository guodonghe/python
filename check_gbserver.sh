#!/bin/bash

# 监控的次数
MONITOR_COUNT=3
# Recv-Q 阈值
THRESHOLD=12399
# 检查间隔（秒）
INTERVAL=1

# 连续超过阈值的计数
count=0

for ((i = 0; i < MONITOR_COUNT; i++)); do
    # 获取当前的 Recv-Q 值
    #recv_q_value=$(netstat -aun | awk '{print $2}' | grep -E '^[0-9]+$' | sort -nr | head -n 1)
    recv_q_value=$(netstat -aun |grep 15060 | awk '{print $2}')

    # 检查 Recv-Q 是否大于阈值
    if [[ "$recv_q_value" -gt "$THRESHOLD" ]]; then
        ((count++))
    else
        count=0
    fi
    #echo $count
    # 如果连续超过阈值，执行 killall 并退出
    if [[ "$count" -ge "$MONITOR_COUNT" ]]; then
        /usr/bin/killall -9 gbserver >/dev/null 2>&1
        exit 0
    fi

    # 等待下一个检查周期
    sleep "$INTERVAL"
done

exit 0


# 另一种方式

#!/bin/bash

# 监控的次数
MONITOR_COUNT=3
# Recv-Q 阈值
THRESHOLD=12399
# 检查间隔（秒）
INTERVAL=1

# 连续超过阈值的计数
count=0

while true; do
    # 获取当前的 Recv-Q 值
    recv_q_value=$(netstat -aun |grep 15060 | awk '{print $2}')
    #recv_q_value=$(netstat -aun |grep 15060 | awk '{print $2}' | grep -E '^[0-9]+$' | sort -nr | head -n 1)

    # 检查 Recv-Q 是否大于阈值
    if [[ "$recv_q_value" -gt "$THRESHOLD" ]]; then
        ((count++))
    else
        count=0
    fi

    # 如果连续三次超过阈值，执行 killall
    if [[ "$count" -ge "$MONITOR_COUNT" ]]; then
        /usr/bin/killall -9 gbserver >/dev/null 2>&1
        count=0  # 重置计数器
    fi

    # 等待下一个检查周期
    sleep "$INTERVAL"
done
