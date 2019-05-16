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
URL = 'http://www.elandmall.com/custcenter/initCustFAQlist.action'

if __name__ == "__main__":
    driver.get(URL)
    time.sleep(3)

    qa_list = []

    first_faq_type = driver.find_element_by_xpath(".//li[@class='faq_large_divi']/a")
    first_faq_type.click()
    time.sleep(3)

    try:
        while True:
            contents = driver.page_source
            html = BeautifulSoup(contents, "html.parser")

            mypage_faq = html.find("div",{"class":"mypage_faq"})
            dl_lists = mypage_faq.find_all("dl")
            for dl in dl_lists:
                #카테고리
                category = html.find("li",{"class": "faq_large_divi selected"}).span.text
                print(category)    
                
                #질문
                question_dt = dl.find('dt')
                for question_tmp in question_dt.span.previous_siblings:            
                    question = question_tmp

                #답변
                answer = dl.find('dd').text.strip()

                #리스트 저장
                qa_list.append([category, question, answer])


            #페이지 이동
            next_pages = driver.find_elements_by_xpath(
            "//span[@class='num']//a[@class='on select_num']/following-sibling::a[@class='num']")
            print(f'next_pages = {len(next_pages)}')

            if len(next_pages) == 0 :

                #대분류 구하깅
                next_divi = driver.find_elements_by_xpath(
                    "//li[@class='faq_large_divi selected']/following-sibling::li[@class='faq_large_divi']/a")
                if(len(next_divi)) == 0:
                    break
                else :
                    next_divi[0].click()
                    time.sleep(3)

            else:
                #스크롤다운
                SCROLL_PAUSE_TIME = 0.5
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)

                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                #페이지 클릭
                next_pages[0].click()
                time.sleep(3)
    finally:
        driver.close()
        dataframe = pandas.DataFrame(qa_list)
        dataframe.to_excel('ElnadMall_FAQ.xlsx',encoding='UTF-8')