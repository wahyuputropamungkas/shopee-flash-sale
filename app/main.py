import json
import time
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

timeout = 60
global inputUrl
global inputIsProductHasVariations
global inputTotalProductVariations
global productVariations
inputUrl = ''
inputIsProductHasVariations = 'n'
inputTotalProductVariations = '0'
productVariations = []

def inputData():
    global inputUrl
    global inputIsProductHasVariations
    global inputTotalProductVariations
    global productVariations

    inputUrl = input(colored('PASTE URL (Ctrl + Shift + C) : ', 'red', attrs=['reverse']))
    inputIsProductHasVariations = input(colored('IS PRODUCT HAS VARIATIONS? (y/n) : ', 'red', attrs=['reverse']))

    productVariations = []

    if inputIsProductHasVariations == 'y':
        if inputTotalProductVariations.isnumeric():
            inputTotalProductVariations = input(colored('TOTAL PRODUCT VARIATIONS : ', 'red', attrs=['reverse']))

            for index in range(int(inputTotalProductVariations)):
                item = input(colored('VARIATION ' + str(index + 1) + ' : ', 'green', attrs=['reverse']))

                productVariations.append(item)

    print(colored('CONFIRMATION! : ', 'blue', attrs=['reverse']))
    print(colored('YOUR PRODUCT URL IS : ' + inputUrl, 'blue', attrs=['reverse']))
    print(colored('IS PRODUCT HAS VARIATIONS? : ' + inputIsProductHasVariations, 'blue', attrs=['reverse']))

    if inputIsProductHasVariations == 'y':
        print(colored('PRODUCT VARIATIONS : ' + str(productVariations), 'blue', attrs=['reverse']))

    isContinue = input(colored('DO YOU WANT TO CONTINUE? (y/n) : ', 'red', attrs=['reverse']))

    if isContinue == 'y':
        scrap()
    else:
        isTryAgain = input(colored('DO YOU WANT TO TRY AGAIN? (y/n) : ', 'red', attrs=['reverse']))

        if isTryAgain == 'y':
            inputData()
        else:
            print(colored('PROGRAM FINISH : ', 'white', attrs=['reverse']))

def scrap():
    global inputUrl
    global productVariations

    print(colored('PROCESS : load page ', 'green', attrs=['reverse']))

    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')
    # options.add_argument("--window-size=1280,720")
    driver = webdriver.Chrome(options=options)

    driver.get(inputUrl)

    print(colored('PROCESS : load cookies ', 'green', attrs=['reverse']))

    try:
        with open('./cookie/cookie.json', 'r') as file:
            cookies = json.load(file)

            for cookie in cookies:
                if 'sameSite' in cookie:
                    if cookie['sameSite'] == 'None' or 'unspecified':
                        cookie['sameSite'] = 'Strict'

                driver.add_cookie(cookie)
    except Exception as e:
        print('ERROR loading cookies! ' + str(e))

    print(colored('PROCESS : refreshing ', 'green', attrs=['reverse']))

    driver.refresh()

    # waiting for shipping button

    waitShippingButton = False

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//div[text()="Pengiriman ke"]')))
        waitShippingButton = True
        print(colored('PROCESS : shipping button ok ', 'green', attrs=['reverse']))
    except Exception as e:
        print(colored('ERROR waiting for shipping choices! ' + str(e), 'red', attrs=['reverse']))

    if not waitShippingButton:
        return True
    
    isVariationsComplete = True

    if len(productVariations) > 0:
        for item in productVariations:
            currentVariation = driver.find_element(By.XPATH, '//button[contains(@class, "product-variation")][text()="' + item + '"]')

            if len(currentVariation) > 0 and currentVariation.is_enabled():
                currentVariation.click()
            else:
                isVariationsComplete = False
                break

    if isVariationsComplete:
        driver.find_element(By.XPATH, '//button[text()="beli sekarang"]').click()
    else:
        print(colored('ERROR incomplete product variations!', 'red', attrs=['reverse']))

        return True

    # waiting for checkout button

    waitCheckoutButton = False

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]')))
        waitCheckoutButton = True
        print(colored('PROCESS : checkout button ok ', 'green', attrs=['reverse']))
    except Exception as e:
        print(colored('ERROR waiting for checkout button! ' + str(e), 'red', attrs=['reverse']))

    if not waitCheckoutButton:
        return True

    driver.find_element(By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]').click()

    # waiting for place order button

    waitBankTransferButton = False

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//button[text()="Transfer Bank"]')))
        waitBankTransferButton = True
        print(colored('PROCESS : bank transfer button ok ', 'green', attrs=['reverse']))
    except Exception as e:
        print(colored('ERROR waiting for bank transfer button! ' + str(e), 'red', attrs=['reverse']))

    if not waitBankTransferButton:
        return True

    driver.find_element(By.XPATH, '//button[text()="Transfer Bank"]').click()

    # waiting for bank mandiri button

    waitBankMandiriButton = False

    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="Bank Mandiri"]')))
        waitBankMandiriButton = True
        print(colored('PROCESS : bank mandiri button ok ', 'green', attrs=['reverse']))
    except Exception as e:
        print(colored('ERROR waiting for bank mandiri button! ' + str(e), 'red', attrs=['reverse']))

    if not waitBankMandiriButton:
        return True

    driver.find_element(By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="Bank Mandiri"]').click()

    waitPlaceOrderButtonClickable = False

    try:
        WebDriverWait(driver, timeout).until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Buat Pesanan"]')))
        waitPlaceOrderButtonClickable = True
        print(colored('PROCESS : place order button is clickable', 'green', attrs=['reverse']))
    except Exception as e:
        print(colored('ERROR place order button not found or unclickable! ' + str(e), 'red', attrs=['reverse']))

    if not waitPlaceOrderButtonClickable:
        return True

    driver.find_element(By.XPATH, '//button[text()="Buat Pesanan"]').click()

    print(colored('PROGRAM SUCCESS! : ', 'green', attrs=['reverse']))

inputData()