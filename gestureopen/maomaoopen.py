import subprocess
import time
import os
import pyautogui

print("启动并最大化窗口...")

program_path = r"D:\maomaoyun\MaoMaoCloud.exe"

if os.path.exists(program_path):
    print("✅ 文件存在")
    
    try:
        # 启动程序 - 使用CREATE_NEW_PROCESS_GROUP让程序独立运行
        print("🚀 启动程序中...")
        process = subprocess.Popen([program_path], 
                                  creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        
        # 等待程序启动
        time.sleep(3)
        
        # 尝试使用快捷键最大化窗口
        print("🔄 尝试最大化窗口...")
        pyautogui.hotkey('win', 'up')  # Windows最大化快捷键
        
        # 等待窗口最大化完成
        time.sleep(2)
        
        # 点击坐标 (1800, 1000)
        print("🖱️ 点击坐标 (1800, 1000)...")
        pyautogui.click(1800, 1000)
        time.sleep(2)
        print("🖱️ 点击坐标 (2453, 1485)...")
        pyautogui.click(2453, 1485)
        
        print("✅ 程序启动、最大化并完成点击操作")
        print("💡 MaoMaoCloud.exe会继续独立运行")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
else:
    print("❌ 文件不存在")

print("📝 脚本执行完毕，自动退出")
# 脚本会自动结束，不需要用户操作