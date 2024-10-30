from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import capture
import ocr
import logging
import configparser
import auto_copy
import os
import threading
import random

def main():
    log_file_path = os.path.join(os.path.expanduser('~'), 'my', 'omega', f'{datetime.now().strftime("%Y%m%d_%H_%M")}.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        filename=log_file_path,
        filemode='a'  # a: add more, w: cover
    )
    # read config
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.expanduser('~'), 'my', 'omega', 'config.ini')
    config.read(config_file_path)
    username = config['credentials']['username']
    password = config['credentials']['password']
    
    try:
        logging.info(' start ')
        # create Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=options)
        
        driver.set_window_size(1100, 1000) # width, height
        driver.set_window_position(450, 0) # x, y

        logging.info(' start: navigate to main page ')

        driver2 = webdriver.Chrome(options=options)
        
        driver2.set_window_size(1100, 1000) # width, height
        driver2.set_window_position(450, 0) # x, y

        # login and arrive the operating page
        thread1 = threading.Thread(target=navigate_to_main_page(driver=driver, username=username, password=password))
        thread2 = threading.Thread(target=navigate_to_main_page(driver=driver2, username='AC655CA', password='AC1331'))
        
        # 啟動執行緒
        thread1.start()
        thread2.start()

        # 等待兩個執行緒結束
        thread1.join()
        thread2.join()

        logging.info(' end: navigate to main page ')


        prev_time = datetime.now()
        count = 1
        stop_count = 0
        last_number = ''
        while True:
            logging.info(' while start ')
            logging.info(f'count: {count}, stop_count: {stop_count}')
            crt_time = datetime.now()
            # end if waiting too long to get a new operating
            if stop_count > 5 and count > 3:
                driver.quit()
                driver2.quit()
                logging.info(' operating end ')
                logging.info(f'count: {count}')
                return
            # this time no operating
            if (crt_time - prev_time).total_seconds() > 20 * 60 and count == 1:
                driver.quit()
                driver2.quit()
                logging.info(' no operating ')
                return
            
            cmd_text = auto_copy.get_string()
            logging.info(f' cmd_text: {cmd_text}')
            number, operator = auto_copy.get_request(cmd_text)

            logging.info(f'number, operator: {number}, {operator}')
            if(number and number != last_number):
                logging.info(' enter ')
                # check current number is website display's number
                crt_number = driver.find_element(By.ID, 'ws6')
                crt_number_val = crt_number.get_attribute("value")
                if(number in crt_number_val):
                    logging.info(' start operating ')
                    try:
                        thread1 = threading.Thread(target=operate(driver=driver, operator=operator))
                        thread2 = threading.Thread(target=operate(driver=driver2, operator=operator))
                        
                        # 啟動執行緒
                        thread1.start()
                        thread2.start()

                        # 等待兩個執行緒結束
                        thread1.join()
                        thread2.join()

                        last_number = number
                        prev_time = crt_time
                        count += 1
                        stop_count = 0
                    except Exception as e:
                        logging.error(f' error: {e}')
                    logging.info(' end operating ')
                else:
                    logging.info('not match!')
                    stop_count += 1
            else:
                logging.info('none or duplicate, pass!')
                stop_count += 1

            time.sleep(10)

    except KeyboardInterrupt:
        logging.warning(" end by myself")
    finally:
        logging.info(" end by system")
        logging.shutdown()
        print("日誌已保存至 .log")


def navigate_to_main_page(driver, username, password):
    # navigate to the login page
    url = 'https://oooo6888.omegasasa.com/login'
    driver.get(url)

    # waiting loading
    driver.implicitly_wait(1)

    # find username and password fields and input
    username_field = driver.find_element(By.XPATH, '(//input[@class="input-content"])[1]')
    password_field = driver.find_element(By.XPATH, '(//input[@class="input-content"])[2]')

    username_field.send_keys(username)
    password_field.send_keys(password)

    # click login button
    login_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')
    login_btn.click()

    time.sleep(5)
    # navigat to the operating page
    url = 'https://oooo6888.omegasasa.com/page-game_financial'
    driver.get(url)

    time.sleep(3)

    select_btn = WebDriverWait(driver, 20, 0.5).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(@onclick, "type=11")]')))
    select_btn.click()

    time.sleep(7)
    driver.switch_to.window(driver.window_handles[-1])

    # get auth
    current_url = driver.current_url
    parsed_url = urlparse(current_url)
    auth_value = parse_qs(parsed_url.query).get("auth", [None])[0]

    url = f'https://lxa94.zue6688.com/techchain/zh_TW/vtech.html?auth={auth_value}&game=1500'
    driver.get(url)
    
    print(f'//span[text()="{username}"]')
    # wait for info displaying
    WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, (f'//span[text()="{username}"]'))))

def operate(driver, operator):
    
    if operator == "低":
        operator_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="wager-form-2"]//div[@class="wager-form-chioce choice"][1]//label[contains(., "低功率")]')))
    else:
        operator_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="wager-form-2"]//div[@class="wager-form-chioce choice"][1]//label[contains(., "高功率")]')))
    
    amount_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "total")))

    print(operator_btn)
    print(amount_input)
    operator_btn.click()
    amount_input.send_keys("200")

    sleep_time = random.uniform(0.5,3.0)
    time.sleep(sleep_time)
    confirm_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="確認檢測"]')))
    confirm_btn.click()

    sleep_time = random.uniform(0.5,3.0)
    time.sleep(sleep_time)

    confirm_again_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="確認"]')))
    print(confirm_again_btn)
    confirm_again_btn.click()
    
    confirm_again2_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="OK"]')))
    confirm_again2_btn.click()
    
    sleep_time = random.uniform(5,7)
    time.sleep(sleep_time)



main()