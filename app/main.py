import json
import time
from datetime import datetime
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from colorama import just_fix_windows_console
import undetected_chromedriver as uc 

timeout = 60
global inputUrl
global inputIsProductHasVariations
global inputTotalProductVariations
global inputPaymentMethod
global productVariations
global isFlashSale
global bankName
inputUrl = ''
inputIsProductHasVariations = 'n'
inputTotalProductVariations = '0'
inputPaymentMethod = 'cod'
productVariations = []
isFlashSale = True
bankName = ''

userAgents = [ 
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
]

def inputData():
    just_fix_windows_console()

    global inputUrl
    global inputIsProductHasVariations
    global inputTotalProductVariations
    global productVariations
    global isFlashSale
    global inputPaymentMethod
    global bankName

    inputUrl = input(colored('PASTE URL (Ctrl + Shift + C) : ', 'red'))
    inputFlashSale = input(colored('IS PRODUCT IN FLASH SALE? (y/n) : ', 'red'))
    inputIsProductHasVariations = input(colored('IS PRODUCT HAS VARIATIONS? (y/n) : ', 'red'))

    productVariations = []

    if inputIsProductHasVariations == 'y':
        if inputTotalProductVariations.isnumeric():
            inputTotalProductVariations = input(colored('TOTAL PRODUCT VARIATIONS : ', 'red'))

            for index in range(int(inputTotalProductVariations)):
                item = input(colored('VARIATION ' + str(index + 1) + ' : ', 'green'))

                productVariations.append(item)

    inputPaymentMethod = input(colored('PAYMENT METHOD (cod / transfer) : ', 'red'))

    if inputPaymentMethod == 'transfer':
        bankName = input(colored('BANK NAME : ', 'red'))

    print(colored('CONFIRMATION! : ', 'blue'))
    print(colored('YOUR PRODUCT URL IS : ' + inputUrl, 'blue'))
    print(colored('IS PRODUCT IN FLASH SALE : ' + inputFlashSale, 'blue'))
    print(colored('IS PRODUCT HAS VARIATIONS? : ' + inputIsProductHasVariations, 'blue'))

    if inputIsProductHasVariations == 'y':
        print(colored('PRODUCT VARIATIONS : ' + str(productVariations), 'blue'))

    print(colored('PAYMENT METHOD : ' + inputPaymentMethod, 'blue'))

    if inputPaymentMethod == 'transfer':
        print(colored('BANK NAME : ' + bankName, 'blue'))

    isContinue = input(colored('DO YOU WANT TO CONTINUE? (y/n) : ', 'red'))

    if isContinue == 'y':
        if inputFlashSale == 'n':
            isFlashSale = False

        scrap()
    else:
        isTryAgain = input(colored('DO YOU WANT TO TRY AGAIN? (y/n) : ', 'red'))

        if isTryAgain == 'y':
            inputData()
        else:
            print(colored('PROGRAM FINISH : ', 'white'))

def scrap():
    global inputUrl
    global productVariations
    global isFlashSale
    global inputPaymentMethod
    global bankName

    print(colored('PROCESS : load page ', 'green'))

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('log-level=3')
    options.add_argument("--window-size=1280,720")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    for agent in userAgents:
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": agent}) 

    driver.get(inputUrl)

    time.sleep(3)

    print(colored('PROCESS : load cookies ', 'green'))

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

    print(colored('PROCESS : refreshing ', 'green'))

    driver.refresh()

    time.sleep(1.5)

    startTime = datetime.now()

    if isFlashSale:
        # waiting for flash sale link to disappear

        try:
            WebDriverWait(driver=driver, timeout=360, poll_frequency=0.2).until(ec.invisibility_of_element_located((By.XPATH, '//a[contains(@href, "/flash_sale")]')))
        except Exception as e:
            print(colored('ERROR waiting flash sale button to disappear! ' + str(e), 'red'))
            
            return True

    # waiting for product variations

    isVariationsComplete = True

    if len(productVariations) > 0:
        for item in productVariations:
            currentVariation = driver.find_elements(By.XPATH, '//button[contains(@class, "product-variation")][@aria-label="' + item + '"][text()="' + item + '"]')

            if len(currentVariation) > 0 and currentVariation[0].is_enabled():
                currentVariation[0].click()
            else:
                isVariationsComplete = False
                break

    if isVariationsComplete:
        try:
            driver.find_element(By.XPATH, '//button[text()="beli sekarang"]').click()
        except Exception as e:
            print(colored('ERROR unable to find order button!', 'red'))
    else:
        print(colored('ERROR incomplete product variations!', 'red'))

        return True

    # waiting for checkout button

    clickedPlaceOrder = datetime.now()

    try:
        WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.2).until(ec.presence_of_element_located((By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]')))
    except Exception as e:
        print(colored('ERROR waiting for checkout button! ' + str(e), 'red'))

        return True

    driver.find_element(By.XPATH, '//button[contains(@class, "shopee-button-solid shopee-button-solid--primary")]/span[text()="checkout"]').click()

    clickedCheckout = datetime.now()

    # waiting for place order button

    if inputPaymentMethod == 'transfer':
        try:
            WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.2).until(ec.presence_of_element_located((By.XPATH, '//button[text()="Transfer Bank"]')))
        except Exception as e:
            print(colored('ERROR waiting for bank transfer button! ' + str(e), 'red'))

            return True

        driver.find_element(By.XPATH, '//button[text()="Transfer Bank"]').click()

        # waiting for bank mandiri button

        try:
            WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.2).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="' + bankName + '"]')))
        except Exception as e:
            print(colored('ERROR waiting for bank mandiri button! ' + str(e), 'red'))

            return True

        driver.find_element(By.XPATH, '//div[contains(@class, "checkout-bank-transfer-item__title") and text()="' + bankName + '"]').click()
    elif inputPaymentMethod == 'cod':
        try:
            WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.2).until(ec.presence_of_element_located((By.XPATH, '//button[text()="COD (Bayar di Tempat)"]')))
        except Exception as e:
            print(colored('ERROR waiting for cod button! ' + str(e), 'red'))

            return True

        driver.find_element(By.XPATH, '//button[text()="COD (Bayar di Tempat)"]').click()
    else:
        print(colored('ERROR unknown payment method!', 'red'))

        return True
    
    choosingPaymentMethod = datetime.now()

    try:
        WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.2).until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Buat Pesanan"]')))
    except Exception as e:
        print(colored('ERROR place order button not found or unclickable! ' + str(e), 'red'))

        return True

    driver.find_element(By.XPATH, '//button[text()="Buat Pesanan"]').click()

    endTime = datetime.now()

    time.sleep(2)

    driver.close()

    print(colored('start -> ' + str(startTime), 'yellow'))
    print(colored('place order -> ' + str(clickedPlaceOrder), 'yellow'))
    print(colored('checkout -> ' + str(clickedCheckout), 'yellow'))
    print(colored('payment method -> ' + str(choosingPaymentMethod), 'yellow'))
    print(colored('end -> ' + str(endTime), 'yellow'))

    print(colored('PROGRAM SUCCESS! : ', 'green'))

inputData()