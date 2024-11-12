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
    clipboard.copy(content)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def run_deprecated_exe(exe_path):
    process = subprocess.Popen(exe_path)
    process.wait()

def extract_from_exe(exe_path, target_file):
    temp_dir = tempfile.gettempdir()
    resource_path = os.path.join(temp_dir, target_file)
    
    if hasattr(sys, '_MEIPASS'):
        resource_path = os.path.join(sys._MEIPASS, target_file)

    shutil.copy(resource_path, temp_dir)
    return os.path.join(temp_dir, target_file)

def delete_resources_folder():
    current_directory = os.getcwd()
    resources_path = os.path.join(current_directory, "resources")
    
    print(f"检查目录: {current_directory}")
    print(f"资源文件夹路径: {resources_path}")

    if os.path.exists(resources_path) and os.path.isdir(resources_path):
        try:
            shutil.rmtree(resources_path)
            print("resources 文件夹及其内容已被删除")
        except Exception as e:
            print(f"删除失败: {e}")
    else:
        print("资源文件夹不存在")

def check_clipboard_for_uuid(target_uuid):
    clipboard_content = clipboard.paste()
    print(f"当前剪切板内容: {clipboard_content}")
    return clipboard_content == target_uuid

def clipboard_monitor(target_uuid):
    while True:
        current_clipboard = clipboard.paste()
        
        if current_clipboard == target_uuid:
            delete_resources_folder()
            print("检测到特定剪切板内容，已删除 resources 文件夹。")
            clipboard.copy("")
            print("已清空剪切板内容。")
            return

def main():
    target_uuid = "cac6ea6f-2004-4ff2-bd2a-a9927cf13018"  # 程序启动完成验证ID，需要跟程序对接

    replace_clipboard_content("14e7f449-fdbd-47b6-8eb6-ffc85a23b6bc")  # 程序启动许可验证ID，需要跟程序对接

    clipboard_thread = threading.Thread(target=clipboard_monitor, args=(target_uuid,))
    clipboard_thread.daemon = True
    clipboard_thread.start()

    exe_path = os.getcwd()
    deprecated_exe_path = os.path.join(exe_path, 'test.exe')
    
    if os.path.exists(deprecated_exe_path):
        zip_path = extract_from_exe(exe_path, 'resources.zip')

        extract_zip(zip_path, exe_path)

        delete_file(zip_path)

        run_deprecated_exe(deprecated_exe_path)

        delete_resources_folder()
    else:
        delete_resources_folder()

    print("程序执行完成。")

if __name__ == "__main__":
    main()
