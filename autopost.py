import json
import threading
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def load_config_file():
    with open('config.json') as data_file:
        return json.load(data_file)

def up_thread(urls, timeLoop, count, driver):
    for i in range(count):
        print(f'up lan:{i+1}/{count}')
        for link in urls:
            driver.get(link + '/up')
            print(link + '  ----> xong')
        currentDateTime = datetime.datetime.now()
        nextTimeToUp = datetime.datetime.now() + datetime.timedelta(minutes=timeLoop)
        print(f'up tiep luc:{nextTimeToUp}')
        time.sleep(timeLoop * 60)
    driver.quit()
def login(username, password, loginPage):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(loginPage)
    usernameBox = driver.find_element_by_id('ctrl_pageLogin_login')
    passwordBox = driver.find_element_by_id('ctrl_pageLogin_password')
    submitBox = driver.find_element_by_css_selector('#pageLogin > dl.ctrlUnit.submitUnit > dd > input')

    usernameBox.send_keys(username)
    passwordBox.send_keys(password)
    submitBox.submit()
    return driver
def main():
    data = load_config_file()
    accounts = data["accounts"]
    upTime = data["count"]
    loginPage = data["loginPage"]
    count = data["count"]
    threads = []
    for item in accounts:
        urls = item["linkup"]
        username = item["username"]
        password = item["password"]
        upInEvery = item["upInEvery"]
        driver = login(username,password,loginPage)
        threads.append(threading.Thread(target=up_thread, args=(urls, upInEvery, count, driver)))
        threads[-1].start()
	
    for thread in threads:
	    thread.join()

if __name__ == '__main__':
    main()
