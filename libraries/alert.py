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
            await telegram_send.send(messages=[("New property: ", property)])
        await telegram_send.send(messages=[(p_extraMessage)])

def extractHref(element):
    if element and type(element) != int:
        try:
            return element["href"]
        except:
            anchor_tag = element.find('a')
            if anchor_tag and type(anchor_tag) != int and 'href' in anchor_tag.attrs:
                return anchor_tag['href']
    else:
        return ""
    
def makeHrefList(p_scrapedVacancies):
    ret = []
    for elem in p_scrapedVacancies:
        href = extractHref(elem)
        if href:
            ret.append(href)
    return ret

def find_new_apartments(old_vacancies, updated_vacancies, p_baseURL, p_useBaseUrl):
    ret = []
    # Exclude the last element
    if updated_vacancies and len(updated_vacancies) > 1 and updated_vacancies[-1] not in old_vacancies:
        updated_vacancies = updated_vacancies[:-1]

    print("------------------------LOG--------------------------")
    print("Checking top elements of ", p_baseURL)
    if old_vacancies and updated_vacancies:
        if p_useBaseUrl:
            print("old = ", p_baseURL + old_vacancies[0])
            print("new = ", p_baseURL+ updated_vacancies[0])
        else:
            print("old = ", old_vacancies[0])
            print("new = ", updated_vacancies[0])
    else:
        print("No href found this time. Most likely the website didn't load correctly")
    print("-----------------------------------------------------")
    

    old_vacancies = [item for item in old_vacancies if item]
    updated_vacancies = [item for item in updated_vacancies if item]
    new_apartments = set(updated_vacancies) - set(old_vacancies)
    
    for property in new_apartments:
        if p_useBaseUrl:
            ret.append(p_baseURL + extractHref(property))
        else:
            ret.append(extractHref(property))

    return ret


def ParsePage(p_userUrl, p_baseUrl ,p_useBaseUrl, p_messageToTheBroker, p_old_page_source, p_className, p_tag):
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)

    soup = BeautifulSoup(p_old_page_source, 'html.parser')

    old_res = soup.find_all(p_tag, {"class": p_className})
    if not old_res:
        old_res = soup.find_all(class_= p_className)

# start parsing
        
    page_source = GetPageSource(p_userUrl, p_className)
    soup = BeautifulSoup(page_source, 'html.parser')
    current_res = soup.find_all(p_tag, {"class": p_className})
    if not current_res:
        current_res = soup.find_all(class_= p_className)

    if current_res:
        old_res = makeHrefList(old_res)
        current_res = makeHrefList(current_res)
        new_apartments = find_new_apartments(old_res, current_res, p_baseUrl, p_useBaseUrl)
        if (not new_apartments):
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(sendTelegramNotification(["test1", "no new partments"], p_messageToTheBroker))
            if old_res:
                old_res = current_res
        else:
            #send notification
            loop = asyncio.get_event_loop()
            loop.run_until_complete(sendTelegramNotification(new_apartments, p_messageToTheBroker))

            old_res = current_res

            #for logging purposes
            print('Nieuwe aanbieding gedetecteerd')
            print(p_userUrl)

    return page_source