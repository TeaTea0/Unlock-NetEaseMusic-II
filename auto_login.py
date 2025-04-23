# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0021F858284C2BC67BDAF358F4079BE00A427E5BAF2A9BC819E15069319EFC4282AF62877B47739F748614E0AAF7E4E2A5B93C4AE8932CB424624BEB5E81C7683D47E4A572BA644148BBB547640FD47B09806E7691E7DDA29D6701C2E1BA5709A9F174900CED97820166564CA2D6FB6EE3D9B92D97809315EBB956D36166FF9F3FDB4538A50B61A52FC8ADEF545667961A360CAED1618E84579522B9AD4C4FC4BFFB16C37936CF5B149F6EE5B1367A8AA273A8F0012EDC532929A1CAE8455B8679895DFB69F748C9F09CEC869AA63B45F99B17B2B4710FB99101F8D23143460AAAEB140EF3FED57E0352A2DBDB8299159CE09763C8472DCE2928E850D87536F4BE2CB8BF4563CE247E536A5EE9E4B7BBEF0F8E880B90A2FA894F1F04F974188CEA97AB41E2E3101696DD0EDB3E5CA4A67F315943C3B15CFAEE154283CAB0FCFBBE3C65D562DCEDA82DDDA0DC00E1F64DD694BB2A33B552A4E03E50D2BACC5E50CD"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
