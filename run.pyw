"""
版权所有 (c) 2024 xiaoxing2009
此代码依据 MIT 许可证获得许可。有关详细信息，请参见项目根目录中的 LICENSE 文件。
项目地址：https://github.com/xiaoxing2009/sb3_anti-decompiling
"""
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import threading
import clipboard

def replace_clipboard_content(content):
    # 替换剪切板内容
    clipboard.copy(content)

def extract_zip(zip_path, extract_to):
    # 解压 zip 文件
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def delete_file(file_path):
    # 删除文件
    if os.path.exists(file_path):
        os.remove(file_path)

def delete_folder(folder_path):
    # 删除文件夹及其内容
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def run_deprecated_exe(exe_path):
    # 运行 Deprecated.exe 并等待其关闭
    process = subprocess.Popen(exe_path)
    process.wait()

def extract_from_exe(exe_path, target_file):
    # 从 EXE 中提取资源文件
    temp_dir = tempfile.gettempdir()
    resource_path = os.path.join(temp_dir, target_file)
    
    # 如果是通过 PyInstaller 打包，资源文件会在 sys._MEIPASS 目录下
    if hasattr(sys, '_MEIPASS'):
        resource_path = os.path.join(sys._MEIPASS, target_file)

    # 将资源文件复制到临时目录
    shutil.copy(resource_path, temp_dir)
    return os.path.join(temp_dir, target_file)

def delete_resources_folder():
    # 删除 resources 文件夹
    current_directory = os.getcwd()
    resources_path = os.path.join(current_directory, "resources")
    
    print(f"检查目录: {current_directory}")  # 调试输出当前目录
    print(f"资源文件夹路径: {resources_path}")  # 调试输出资源文件夹路径

    if os.path.exists(resources_path) and os.path.isdir(resources_path):
        try:
            shutil.rmtree(resources_path)
            print("resources 文件夹及其内容已被删除")
        except Exception as e:
            print(f"删除失败: {e}")
    else:
        print("资源文件夹不存在")

def check_clipboard_for_uuid(target_uuid):
    # 检查剪切板是否包含目标 UUID
    clipboard_content = clipboard.paste()
    print(f"当前剪切板内容: {clipboard_content}")  # 调试输出当前剪切板内容
    return clipboard_content == target_uuid

def clipboard_monitor(target_uuid):
    # 在独立线程中监控剪切板内容
    while True:
        # 检查剪切板内容
        current_clipboard = clipboard.paste()
        
        # 如果剪切板内容与目标 UUID 匹配，删除资源文件夹
        if current_clipboard == target_uuid:
            delete_resources_folder()
            print("检测到特定剪切板内容，已删除 resources 文件夹。")
            clipboard.copy("")  # 清空剪切板内容
            print("已清空剪切板内容。")
            return  # 删除完成后退出线程

def main():
    target_uuid = "cac6ea6f-2004-4ff2-bd2a-a9927cf13018"  # 程序启动完成验证ID，需要跟程序对接

    # 替换剪切板内容
    replace_clipboard_content("14e7f449-fdbd-47b6-8eb6-ffc85a23b6bc")  # 程序启动许可验证ID，需要跟程序对接

    # 创建并启动剪切板监控线程
    clipboard_thread = threading.Thread(target=clipboard_monitor, args=(target_uuid,))
    clipboard_thread.daemon = True  # 设置为守护线程，主程序退出时自动退出
    clipboard_thread.start()

    # 主程序可以继续进行其他任务，例如运行 Deprecated.exe
    exe_path = os.getcwd()  # 获取当前程序目录
    deprecated_exe_path = os.path.join(exe_path, 'test.exe')
    
    if os.path.exists(deprecated_exe_path):
        # 提取 resources.zip
        zip_path = extract_from_exe(exe_path, 'resources.zip')  # 从 EXE 提取资源文件

        # 解压到程序所在目录
        extract_zip(zip_path, exe_path)

        # 删除 resources.zip
        delete_file(zip_path)

        # 运行 Deprecated.exe
        run_deprecated_exe(deprecated_exe_path)

        # 清理操作
        delete_resources_folder()
    else:
        # 如果 Deprecated.exe 不存在，直接删除 resources 文件夹
        delete_resources_folder()

    # 程序完成后退出
    print("程序执行完成。")

if __name__ == "__main__":
    main()
