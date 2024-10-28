import pyautogui
import pyperclip
import time
from PIL import ImageGrab

def get_string():
    # first time to find text
    pyautogui.moveTo(230, 732, duration=1)
    pyautogui.click() # focus on the window

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
    if '單號' in text and '+2' in text:
        number = text[text.index('單號') + len('單號'):text.index('單號') + len('單號') + 5]
        operator = text[text.index('+2') - 1]
        return number, operator
    return None, None

# get_string()
# print(get_request(get_string()))