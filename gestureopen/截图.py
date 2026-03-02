import pyautogui
import os
import time
from datetime import datetime

# 创建截图目录（如果不存在）
screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# 生成带时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{screenshot_dir}/screenshot_{timestamp}.png"

try:
    # 截屏
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"截图已保存: {filename}")

    # 截图成功，无弹窗通知
except Exception as e:
    print(f"截图失败: {e}")

    # 错误情况，无弹窗通知

print("截图脚本执行完毕")
