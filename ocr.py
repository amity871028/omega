from PIL import Image
import pytesseract

def get_string(screenshot_path):
    img = Image.open(f'screenshot/{screenshot_path}.png')
    text = pytesseract.image_to_string(img, lang="chi_tra+eng")
    clean_text = text.replace(' ', '')
    return clean_text

def get_request(text):
    if ('單號' in text or '00' in text) and ('+2' in text or '十2' in text or '42'):
        if '單號' in text:
            number = text[text.index('單號') + len('單號'):text.index('單號') + len('單號') + 5]
        else:
            number = text[text.index('00') + len('00') - 2:text.index('00') + len('00') + 5]
        if '+2' in text:
            operator = text[text.index('+2') - 1]
        elif '十2' in text:
            operator = text[text.index('十2') - 1]
        else:
            operator = text[text.index('42') - 1]
        return number, operator
    return None, None


# clean_text = get_string('20241028_12_52_1')
# number, operator = get_request(clean_text)
# print(clean_text)
# print(number, operator)