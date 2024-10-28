import pyautogui
import time
def save_screenshot(screenshot_name):
    # 截圖保存路徑
    screenshot_path = f'screenshot/{screenshot_name}.png'

    x = 146
    y = 782
    width = 240
    height = 60

    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(screenshot_path)

# time.sleep(1)
# save_screenshot('test3')
# print(pyautogui.position())