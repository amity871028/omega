from PIL import Image
import pytesseract

def get_string(screenshot_path):
    img = Image.open(f'screenshot/{screenshot_path}.png')
    text = pytesseract.image_to_string(img, lang="chi_tra+eng")
    clean_text = text.replace(' ', '')
    return clean_text

def get_request(text):
    if '單號' in text and '+2' in text:
        number = text[text.index('單號') + len('單號'):text.index('單號') + len('單號') + 5]
        operator = text[text.index('+2') - 1]
        return number, operator
    return None, None


# clean_text = get_string('test.png')
# number, operator = get_request(clean_text)
# print(clean_text)
# print(number, operator)