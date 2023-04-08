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
url = 'https://shopee.co.id/Terwuwu-kemeja-panjang-pria-cowok-gatlemen-cowok-biru-navy-dongker-polos-formal-kantor-i.193771301.16641731058'
productName = 'kemeja panjang pria'
productUrl = 'kemeja-panjang-pria'

def scrap():
    print('load homepage...')

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
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

    # waitFlashSaleLink = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//a[contains(@class, "shopee-header-section__header-link")]')))

    # driver.find_element(By.XPATH, '//a[contains(@class, "shopee-header-section__header-link")][contains(@href, "/flash_sale")]').click()

    # try:
    #     waitProductLink = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//a[contains(@href, "' + productUrl + '")]')))
    # except Exception as e:
    #     print(str(e))

    # print('-------------- A1 ------------------')
    # print(driver.current_url)

    # driver.find_element(By.XPATH, '//a[contains(@href, "' + productUrl + '")]').click()

    # try:
    #     waitBuyButton = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[text()="beli sekarang"]')))
    # except Exception as e:
    #     print(str(e))

    try:
        waitShippingButton = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//div[text()="Pengiriman ke"]')))
    except Exception as e:
        print(str(e))

    print('-------------- A2 ------------------')
    print(driver.current_url)

    driver.find_element(By.XPATH, '//button[contains(@class, "product-variation")][text()="Navy Pendek"]').click()

    driver.find_element(By.XPATH, '//button[contains(@class, "product-variation")][text()="M"]').click()

    driver.find_element(By.XPATH, '//button[text()="beli sekarang"]').click()

    # try:
    #     waitRedirect = WebDriverWait(driver, timeout).until(ec.url_changes(url))
    # except Exception as e:
    #     print(str(e))

    # print('-------------- A3 ------------------')
    # print(driver.current_url)

    try:
        waitCheckoutButton = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]')))
    except Exception as e:
        print(str(e))

    print('-------------- A4 ------------------')
    print(driver.current_url)

    driver.find_element(By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]').click()

    try:
        waitOrderButton = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[text()="Buat Pesanan"]')))
    except Exception as e:
        print(str(e))

    print('-------------- A5 ------------------')
    print(driver.current_url)

    try:
        waitPaymentMethodButton = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[text()="Transfer Bank"]')))
    except Exception as e:
        print(str(e))

    print('-------------- A6 ------------------')
    print(driver.current_url)

    driver.find_element(By.XPATH, '//button[text()="Transfer Bank"]').click()

    try:
        waitBankButton = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="Bank Mandiri"]')))
    except Exception as e:
        print(str(e))

    driver.find_element(By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="Bank Mandiri"]').click()

    # try:
    #     waitRadioButton = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "stardust-radio-button stardust-radio-button--checked")]')))
    # except Exception as e:
    #     print(str(e))

    time.sleep(3)

    driver.find_element(By.XPATH, '//button[text()="Buat Pesanan"]').click()

    print('-------------- A7 ------------------')
    print(driver.current_url)

scrap()