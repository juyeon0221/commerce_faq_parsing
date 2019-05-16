import time
import pandas

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
URL = 'https://www.giordano.co.kr/Customer/faq.asp#'

if __name__ == "__main__":
    driver.get(URL)
    time.sleep(3)
    
    qa_list = []

    try:
        while True:
            contents = driver.page_source
            html = BeautifulSoup(contents, "html.parser")

            tr_elements = html.find_all('tr', {'class': 'first'})
            print(tr_elements)
            for tr in tr_elements:
                #카테고리
                td_list = tr.find_all('td')
                category = td_list[1].text
                print(category)
                    
                #질문
                question_td = tr.find('td',{'class':'tit'})
                question = question_td.text
                print(question)
                
                driver.find_element_by_xpath(
                    "//td[@class='tit']//a").click()

                #답변
                answer_contents = driver.page_source
                answer_html = BeautifulSoup(answer_contents, "html.parser")

                answer = answer_html.find('div',{'class':'view_cont'}).text.strip()
                print(answer)

                #리스트 저장
                qa_list.append([category, question, answer])

                driver.find_element_by_xpath(
                    "//div[@class='btn_right01']//a").click()

                contents = driver.page_source
                html = BeautifulSoup(contents, "html.parser")

            # 페이지 이동
            next_pages = driver.find_elements_by_xpath("//div[@id='ui_page_skip']//a[@class='on']/following-sibling::a[@onclick='Pager']")
            if len(next_pages) == 0 :
                print('no pages')
                break
            else:
                next_pages[0].click()
                time.sleep(3)
    finally:
        driver.close()
        dataframe = pandas.DataFrame(qa_list)
        dataframe.to_excel('giordano.xlsx',encoding='UTF-8')
