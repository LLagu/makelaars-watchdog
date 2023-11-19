from bs4 import BeautifulSoup
import time
import telegram_send
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import warnings
import asyncio

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from libraries.file_management import *

def GetPageSource(p_userUrl, p_className):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        driver = webdriver.Firefox(options=options)
    
    try:
        driver.set_page_load_timeout(120)
        driver.get(p_userUrl)
     
        # WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, p_className)))
        # WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//body[not(@class="loading")]')))

        pageSource = driver.page_source
        
    except Exception as e:
        print(f"Failed to retrieve page source. Please check your connection..Error during page navigation: {e}")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(sendTelegramNotification([], "Failed to retrieve page source. Please check your connection."))
        
        pageSource = None

    finally:
        driver.quit()
    
    return pageSource


async def sendTelegramNotification(p_apartmentsList, p_extraMessage):
        for property in p_apartmentsList:
            #By using the *property syntax, it unpacks the elements of the property list, and they will be passed as separate arguments to the send function.
            await telegram_send.send(messages=[("New property: ", *property)])
        await telegram_send.send(messages=[(p_extraMessage)])

def extractHref(element):
    try:
        return element["href"]
    except:
        anchor_tag = element.find('a')
        if anchor_tag and 'href' in anchor_tag.attrs:
            return anchor_tag['href']

def find_new_apartments(old_vacancies, updated_vacancies, p_baseURL):
    ret = []
    # Exclude the last element
    if updated_vacancies and updated_vacancies[-1] not in old_vacancies:
        updated_vacancies = updated_vacancies[:-1]

    print("------------------------LOG--------------------------")
    print("Checking ", p_baseURL)
    print("old = ", extractHref(old_vacancies[0]))
    print("new = ",extractHref(updated_vacancies[0]))
    print("-----------------------------------------------------")
    new_apartments = set(updated_vacancies) - set(old_vacancies)
    
    for property in new_apartments:
        # ret.append(property.find['href'])
        ret.append(extractHref(property))
    return ret

def ParsePage(p_userUrl, p_baseUrl ,p_messageToTheBroker, p_old_page_source, p_className, p_tag):
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)

    soup = BeautifulSoup(p_old_page_source, 'html.parser')
    old_res = soup.find_all(p_tag, {"class": p_className})

# start parsing
        
    page_source = GetPageSource(p_userUrl, p_className)
    soup = BeautifulSoup(page_source, 'html.parser')
    current_res = soup.find_all(p_tag, {"class": p_className})

    if current_res:
        
        new_apartments = find_new_apartments(old_res, current_res, p_baseUrl)
        if (not new_apartments):
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(sendTelegramNotification(["test1", "no new partments"], p_messageToTheBroker))
            old_res = current_res
        else:
            #send notification
            loop = asyncio.get_event_loop()
            loop.run_until_complete(sendTelegramNotification(new_apartments, p_messageToTheBroker))

            #for logging purposes
            print('Nieuwe aanbieding gedetecteerd')
            print(p_userUrl)

    return page_source