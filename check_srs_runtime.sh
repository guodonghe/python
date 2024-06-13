#!/bin/bash

# 查找srs进程的PID
srs_pid=$(pgrep srs)

# 检查srs进程是否存在
if [ -z "$srs_pid" ]; then
  echo "srs process is not running."
  exit 1
fi

# 获取srs进程的运行时间
srs_runtime=$(ps -p $srs_pid -o etime=)

# 显示srs进程的运行时间
echo "srs process has been running for $srs_runtime"
