import time
import pandas
import re

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
options.add_argument('no-sandbox')
options.add_argument('disable-dev-shm-usage')
# options.add_argument(f'user-agent={generate_user_agent()}')

chromedriver_path = 'D:/python/workspace/chromedriver.exe'
driver = webdriver.Chrome(chromedriver_path, options=options)
URL = 'https://www.tbhshop.co.kr/board/?page=1&db=basic_2'


if __name__ == "__main__":
    driver.get(URL)
    time.sleep(3)
    
    qa_list = []

    try:
        while True:
            contents = driver.page_source
            html = BeautifulSoup(contents, "html.parser")

            tbody = html.find('tbody')
            q_lists = tbody.find_all('tr', {'class': re.compile(r'title')})
            a_lists = tbody.find_all('div',{'class': 'cnt'})
            
            i = 0
            for i in range(len(q_lists)) :
                qa_list.append([q_lists[i].text, a_lists[i].text])
                print(qa_list)
                i = i+1

            # 페이지 이동
            next_pages = driver.find_elements_by_xpath("//ul[@class='paging']//strong/ancestor::li/following-sibling::li//a")
            if len(next_pages) == 0 :
                print('no pages')
                break
            else:
                next_pages[0].click()
                time.sleep(3)
    finally:
        driver.close()
        dataframe = pandas.DataFrame(qa_list)
        dataframe.to_excel('mindBridge.xlsx',encoding='UTF-8')
