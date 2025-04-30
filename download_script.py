import requests
import os
import time # 引入 time 模块，可以在每次下载间添加延迟

# --- 配置 ---
# 要下载的文件的 URL
file_url = "https://ovopark.oss-cn-hangzhou.aliyuncs.com/web/download/IPCSearch3.0Setup.exe"
# 下载次数
download_count = 10
# 保存文件的目录 (如果不存在，脚本会尝试创建)
save_directory = "downloads"
# 可选：每次下载之间的延迟（秒），防止过于频繁请求
delay_between_downloads = 1 # 延迟1秒

# --- 脚本执行 ---

def download_file(url, save_path):
    """下载单个文件并保存到指定路径"""
    try:
        print(f"Attempting to download from {url} to {save_path}...")
        # 发起 GET 请求，stream=True 用于处理大文件
        response = requests.get(url, stream=True, timeout=60) # 设置超时时间为60秒

        # 检查请求是否成功 (状态码 200)
        response.raise_for_status() # 如果状态码不是 200，会抛出 HTTPError 异常

        # 以二进制写模式打开本地文件
        with open(save_path, 'wb') as f:
            # 分块写入文件内容
            for chunk in response.iter_content(chunk_size=8192): # 每次写入 8KB
                if chunk: # 过滤掉 keep-alive 新块
                    f.write(chunk)
        print(f"Successfully downloaded: {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        # 如果下载失败，尝试删除可能已创建的不完整文件
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
                print(f"Removed incomplete file: {save_path}")
            except OSError as remove_error:
                print(f"Error removing incomplete file {save_path}: {remove_error}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while downloading {url}: {e}")
        return False
def main():
    """主函数，执行多次下载"""
    # 确保保存目录存在
    if not os.path.exists(save_directory):
        try:
            os.makedirs(save_directory)
            print(f"Created directory: {save_directory}")
        except OSError as e:
            print(f"Error creating directory {save_directory}: {e}")
            return # 如果无法创建目录，则退出

    # 从 URL 中提取原始文件名和扩展名
    try:
        original_filename = os.path.basename(file_url.split('?')[0]) # 去掉可能的 URL 参数
        filename_base, file_extension = os.path.splitext(original_filename)
    except Exception as e:
        print(f"Could not parse filename from URL '{file_url}': {e}")
        # 使用默认名称，如果无法解析
        filename_base = "downloaded_file"
        file_extension = ""


    successful_downloads = 0
    # 循环下载指定次数
    for i in range(1, download_count + 1):
        # 构建每次下载的文件名 (例如: IPCSearch3.0Setup_1.exe)
        new_filename = f"{filename_base}_{i}{file_extension}"
        save_path = os.path.join(save_directory, new_filename)

        print(f"\n--- Download Attempt {i}/{download_count} ---")
        if download_file(file_url, save_path):
            successful_downloads += 1

        # 如果不是最后一次下载，并且设置了延迟，则等待
        if i < download_count and delay_between_downloads > 0:
            print(f"Waiting for {delay_between_downloads} seconds before next download...")
            time.sleep(delay_between_downloads)

    print(f"\n--- Download Summary ---")
    print(f"Finished. Attempted {download_count} downloads.")
    print(f"Successfully downloaded {successful_downloads} files.")
    print(f"Files saved in directory: {os.path.abspath(save_directory)}")

# 当脚本直接运行时，调用 main 函数
if __name__ == "__main__":
    main()
