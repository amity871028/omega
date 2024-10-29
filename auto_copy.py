import pyautogui
import pyperclip
import time
from PIL import ImageGrab

def get_string():
    pyautogui.moveTo(476, 788, duration=1) # prevent unread text display
    pyautogui.click() # focus on the window
    time.sleep(0.5)

    # first time to find text
    pyautogui.moveTo(230, 732, duration=1)

    time.sleep(1)
    pyautogui.click(clicks=3) # select all

    time.sleep(1)
    # pyautogui.hotkey('command', 'c') # macOS
    pyautogui.hotkey('ctrl', 'c')  # copy third times to make sure copy success
    pyautogui.hotkey('ctrl', 'c') 
    pyautogui.hotkey('ctrl', 'c') 

    # second time to find text
    pyautogui.moveTo(230, 752, duration=1)

    time.sleep(1)
    pyautogui.click(clicks=3) # select all

    time.sleep(1)
    # pyautogui.hotkey('command', 'c') # macOS
    pyautogui.hotkey('ctrl', 'c')  # copy third times to make sure copy success
    pyautogui.hotkey('ctrl', 'c') 
    pyautogui.hotkey('ctrl', 'c') 
    
    time.sleep(1)

    try:
        copied_text = pyperclip.paste()
        clean_text = copied_text.replace(' ', '')
        print("clean_text:", clean_text)
        return clean_text
    except pyperclip.PyperclipException as e:
        print("error:", e)

def get_request(text):
    if ('０' in text or '0' in text) and ('高' in text or '低' in text):
        if '0' in text:
            number = text[text.index('0') + len('0') - 1:text.index('0') + len('0') + 4]
        else:
            number = text[text.index('０') + len('０') - 1:text.index('０') + len('０') + 4]
            number = number.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
        if '高' in text:
            operator = '高'
        else:
            operator = '低'
        return number, operator
    return None, None

# print(pyautogui.position())
# get_string()
# print(get_request(get_string()))
# from datetime import datetime
# prev_time = datetime.now()
# time.sleep(10)
# crt_time = datetime.now()
# print((crt_time - prev_time).total_seconds())