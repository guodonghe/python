import json
import re
from datetime import datetime, timedelta

log_files = [
    "artisan_business_play_advert_report.log",
    "artisan_business_play_advert_report.log.1",
    "artisan_business_play_advert_report.log.2",
    "artisan_business_play_advert_report.log.3"
]

# 设置日期范围
start_date = "2025-05-19"
end_date = "2025-05-21"

# 生成日期范围内的所有日期
start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")
date_range = []
current = start
while current <= end:
    date_range.append(current.strftime("%Y-%m-%d"))
    current += timedelta(days=1)

# 为每个日期创建计数器
stats = {}
for date in date_range:
    stats[date] = {
        'ios_count': 0,
        'android_count': 0,
        'total_count': 0
    }

# 提取 {...} 的 JSON 正则
json_pattern = re.compile(r'\{.*\}')

for filename in log_files:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                # 检查是否包含日期范围内的任何日期
                if any(date in line for date in date_range) and ('"return_advert":"1"' in line or '"return_advert":1' in line):
                    match = json_pattern.search(line)
                    if match:
                        try:
                            data = json.loads(match.group())
                            platform = data.get("platform", "").lower()
                            return_advert = data.get("return_advert")
                            report_time = data.get("report_time", "")

                            # 检查return_advert的值（可能是字符串"1"或数字1）
                            is_valid_return = (
                                return_advert == "1" or
                                return_advert == 1 or
                                str(return_advert) == "1"
                            )

                            if is_valid_return:
                                # 检查日期是否在范围内
                                for date in date_range:
                                    if date in report_time:
                                        if platform == "ios":
                                            stats[date]['ios_count'] += 1
                                        elif platform == "android":
                                            stats[date]['android_count'] += 1
                                        stats[date]['total_count'] += 1
                                        break
                        except json.JSONDecodeError:
                            continue
                            continue
    except FileNotFoundError:
        print(f"文件 {filename} 未找到，跳过...")

# 打印统计结果
print(f'统计日期范围：{start_date} 到 {end_date}\n')
for date in date_range:
    print(f'日期: {date}')
    print(f'iOS平台 ("return_advert":"1") 的次数: {stats[date]["ios_count"]}')
    print(f'Android平台 ("return_advert":1) 的次数: {stats[date]["android_count"]}')
    print(f'总次数: {stats[date]["total_count"]}')
    print('-' * 50)

# 打印总计
total_ios = sum(stats[date]['ios_count'] for date in date_range)
total_android = sum(stats[date]['android_count'] for date in date_range)
total_all = sum(stats[date]['total_count'] for date in date_range)

print('\n总计:')
print(f'iOS平台总次数: {total_ios}')
print(f'Android平台总次数: {total_android}')
print(f'所有平台总次数: {total_all}')
