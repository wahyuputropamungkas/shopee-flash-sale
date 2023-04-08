import os
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

timeout = 60
url = 'https://shopee.co.id/SANDAL-DISTRO-PRIA-CASUAL-KEKINIAN-i.367732093.16669092439'

def scrap():
    print('load homepage...')

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,720")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try:
        with open('./cookie/cookie.json', 'r') as file:
            cookies = json.load(file)

            for cookie in cookies:
                if 'sameSite' in cookie:
                    if cookie['sameSite'] == 'None' or 'unspecified':
                        cookie['sameSite'] = 'Strict'

                driver.add_cookie(cookie)
    except Exception as e:
        print('-------------------- ' + str(e))

    driver.refresh()
    time.sleep(5)

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//div[text()="Pengiriman ke"]')))
    except Exception as e:
        print(str(e))

    driver.find_element(By.XPATH, '//button[contains(@class, "product-variation")][text()="Hitam"]').click()

    driver.find_element(By.XPATH, '//button[contains(@class, "product-variation")][text()="40"]').click()

    driver.find_element(By.XPATH, '//button[text()="beli sekarang"]').click()

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]')))
    except Exception as e:
        print(str(e))

    driver.find_element(By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]').click()

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[text()="Buat Pesanan"]')))
    except Exception as e:
        print(str(e))

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[text()="Transfer Bank"]')))
    except Exception as e:
        print(str(e))

    driver.find_element(By.XPATH, '//button[text()="Transfer Bank"]').click()

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="Bank Mandiri"]')))
    except Exception as e:
        print(str(e))

    driver.find_element(By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="Bank Mandiri"]').click()

    time.sleep(3)

    driver.find_element(By.XPATH, '//button[text()="Buat Pesanan"]').click()

    print('finish')

scrap()