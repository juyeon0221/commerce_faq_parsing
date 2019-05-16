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
URL = 'https://www.forever21.co.kr/CustomerService/CustomerService.aspx?br=f21'


if __name__ == "__main__":
    driver.get(URL)
    time.sleep(3)
    
    qa_list = []

    contents = driver.page_source
    html = BeautifulSoup(contents, "html.parser")

    selection_elements = html.select("section.ac-container > div")
    for selection in selection_elements:
        #카테고리
        category = selection.find('label',{'id':'ac-title'}).text

        qa_elements = selection.select('article.ac-small > div')
        for qa_element in qa_elements:
            #질문
            question = qa_element.find('label',{'id':'ac-title'}).text.strip()
            print(f'{category} :{question}')

            #답변
            answer = qa_element.find('article',{'class':'ac-small'}).text.strip()
            print(answer)

            #리스트 저장
            qa_list.append([category, question, answer])
    
    #파일저장
    driver.close()
    dataframe = pandas.DataFrame(qa_list)
    dataframe.to_excel('29cm_FAQ.xlsx',encoding='UTF-8')
