from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def show_detail(driver):
    last_page = get_last_page()

    for i in range(last_page):
        # 의약품 테이블의 tr태그 개수를 세기 위함
        tbody = driver.find_element(By.XPATH, '//*[@id="con_body"]/div[2]/div[3]/div[3]/table/tbody')
        number_of_row = len(tbody.find_elements(By.TAG_NAME, 'tr'))

        # 조회결과가 없을 때 함수 종료
        if number_of_row == 1:
            return
        print(number_of_row)

        ######테스트용 number_of_row
        number_of_row = 1

        # tr태그 개수 만큼 반복
        for j in range(1, number_of_row + 1):
            name = driver.find_element(By.XPATH,
                                       f'//*[@id="con_body"]/div[2]/div[3]/div[3]/table/tbody/tr[{j}]/td[2]/span[2]/a')
            popup_URL = name.get_attribute('href')
            print(popup_URL)
            driver.get(url=popup_URL)

            ######테스트용 dict
            save_tester = {}
            for k in range(1,5):
                title_xpath = f'//*[@id="content"]/section/div[1]/div[2]/table/tbody/tr[{k}]/th'
                contents_xpath = f'//*[@id="content"]/section/div[1]/div[2]/table/tbody/tr[{k}]/td'
                title = driver.find_element(By.XPATH, title_xpath)
                contents = driver.find_element(By.XPATH, contents_xpath)
                save_tester[title.text]=contents.text
            print(save_tester)

# 최대 페이지 정보를 얻기 위함.(onclick attribute의 value이용)
def get_last_page():
    try:
        last_page = driver.find_element(By.CLASS_NAME, 'page_last')
        last_page_onclick_value = last_page.get_attribute('onclick')
        if not last_page_onclick_value:
            return 1
        print(last_page_onclick_value)

        # value에서 정수만을 추출하기 위함
        splited_value = last_page_onclick_value.split('(')
        print(splited_value[1][:-1])
        # return splited_value
        return 1  # 테스트 용 리턴값
    except:
        # 항목이 없을 경우
        return 1


def mfds_total_drug(driver):
    # 약학정보원 의약품 전체 검색

    # 의약품안전나라(식약처) URL
    URL = 'https://nedrug.mfds.go.kr/searchDrug'

    driver.get(url=URL)

    print(driver.current_url)

    # 낱알검색 버튼
    pill_button = driver.find_element(By.XPATH, '//*[@id="con_body"]/div[2]/div[2]/div[1]/ul/li[2]/a')

    pill_button.click()

    # 타입별 데이터 갯수저장할 list (테스트용)
    # number_of_drug_by_type = []

    # 최하단 검색 버튼의 xpath
    search_xpath = '//*[@id="searchGrain"]/fieldset/div[8]/button[1]'
    search = driver.find_element(By.XPATH, search_xpath)

    for i in range(2, 3): #original stop number-> 12 / tester stop number-> 3
        # 알약 타입 클릭 -> 검색 클릭
        type = driver.find_element(By.XPATH, f'//*[@id="drugShapeList"]/li[{i}]/a')
        type.click()
        # explictly waits 로딩되기 전 먼저 실행되는 걸 방지하기 위함.
        search = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )
        search.click()

        show_detail(driver)
    #     #타입별 갯수
    #     count = driver.find_element(By.XPATH, '//*[@id="con_body"]/div[2]/div[3]/div[2]/p/strong')
    #     number_of_drug_by_type.append(count.text)
    #
    # for i in range(len(number_of_drug_by_type)):
    #     print(f'type{i + 1}의 의약품 갯수: {number_of_drug_by_type[i]}')
