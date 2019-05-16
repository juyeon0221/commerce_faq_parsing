import time
import pandas

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

driver = webdriver.Chrome('D:/python/workspace/chromedriver.exe')
#driver = webdriver.Chrome()

URL = 'https://www.topten10mall.com/kr/front/customer/faqList.do'


if __name__ == "__main__":
    driver.get(URL)
    time.sleep(3)

    qa_list = []

    try:
        while True:
            contents = driver.page_source
            html = BeautifulSoup(contents, "html.parser")

            mytable_elements = html.select("ul.body>li")
            for mytable_element in mytable_elements:
                #카테고리
                category= mytable_element.find('span',{'class':'type'}).text
                print(category)
                    
                #질문
                question= mytable_element.find('span',{'class':'title'}).text
                print(question)

                #답변
                answer = mytable_element.find('div',{'class':'answer'}).text
                print(answer)

                #리스트 저장
                qa_list.append([category, question, answer])

            # 페이지 이동
            next_pages = driver.find_elements_by_xpath(
                "//ul[@class='pagination']//a[@class='active']/ancestor::li/following-sibling::li//a[@class='num']")
            if len(next_pages) == 0 :
                print('no pages')
                break
            else:
                next_pages[0].click()
                time.sleep(3)
    finally:
        driver.close()
        dataframe = pandas.DataFrame(qa_list)
        dataframe.to_excel('TOPTEN_FAQ.xlsx',encoding='UTF-8')