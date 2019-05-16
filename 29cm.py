import time
import pandas

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

driver = webdriver.Chrome('D:/python/workspace/chromedriver.exe')
#driver = webdriver.Chrome()

url='https://www.29cm.co.kr/mypage/cscenter/faq-cs/faq-list'

if __name__ == "__main__":
    driver.get(url)
    time.sleep(3)
    
    qa_list = []

    try:
        while True:
            contents = driver.page_source
            html = BeautifulSoup(contents, "html.parser")

            mytable_elements = html.select("div[class=my_tbl]")
            for mytable_element in mytable_elements:
                #카테고리
                category_p = mytable_element.find('p',{'class':'type'})
                for category_tmp in category_p.span.next_siblings:            
                    category = category_tmp
                    
                #질문
                question_p = mytable_element.find('p',{'class':'tit'})
                for question_tmp in question_p.span.next_siblings:            
                    question = question_tmp
                #답변
                answer_p = mytable_element.find('div',{'class':'a_wrap'}).text
                answer = answer_p.strip()

                #리스트 저장
                qa_list.append([category, question, answer])

            # 페이지 이동
            next_pages = driver.find_elements_by_xpath("//span[@class='num current']/following-sibling::span[@class='num']//a")
            if len(next_pages) == 0 :
                print('no pages')
                break
            else:
                next_pages[0].click()
                time.sleep(3)
    finally:
        driver.close()
        dataframe = pandas.DataFrame(qa_list)
        dataframe.to_excel('29cm_FAQ.xlsx',encoding='UTF-8')
