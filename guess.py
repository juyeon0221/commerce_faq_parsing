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
URL = 'https://www.guesskorea.com/front/customer_faq.php?block=0&gotopage=1&category=all'


if __name__ == "__main__":
    driver.get(URL)
    time.sleep(3)
    
    qa_list = []

    try:
        while True:
            contents = driver.page_source
            html = BeautifulSoup(contents, "html.parser")

            mytable_elements = html.select("ul[class=faq_toggle] > li")
            for mytable_element in mytable_elements:
                    
                #질문
                question= mytable_element.find('div',{'class':'q_area'}).a.text.strip()
                print(question)

                #답변
                answer= mytable_element.find('div',{'class':'a_area'}).text.strip()
                print(answer)

                #리스트 저장
                qa_list.append([question, answer])

            # 페이지 이동
            next_pages = driver.find_elements_by_xpath("//div[@class='list-paginate']//a[@class='on']/following-sibling::a")
            if len(next_pages) - 2 == 0 :
                print('no pages')
                break
            else:
                next_pages[0].click()
                time.sleep(3)
    finally:
        driver.close()
        dataframe = pandas.DataFrame(qa_list)
        dataframe.to_excel('guess.xlsx',encoding='UTF-8')
