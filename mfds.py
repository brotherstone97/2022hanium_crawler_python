from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def show_detail(driver):
    #의약품 테이블의 tr태그 개수를 세기 위함
    # tbody = driver.find_element(By.XPATH, '//*[@id="con_body"]/div[2]/div[3]/div[3]/table/tbody')
    # number_of_row = len(tbody.find_elements(By.TAG_NAME, 'tr'))
    #
    # #조회결과가 없을 때 함수 종료
    # if number_of_row==1:
    #     return
    # print(number_of_row)
    #
    # #tr태그 개수 만큼 반복
    # for i in range(1, number_of_row + 1):
    #     name = driver.find_element(By.XPATH,
    #                                f'//*[@id="con_body"]/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[2]/span[2]/a')
    #     print(name.text)

    #다음페이지로 이동
    last_page = driver.find_element(By.CLASS_NAME, 'page_last')
    last_page_onclick_value = last_page.get_attribute('onclick')
    if not last_page_onclick_value:
        return
    print(last_page_onclick_value)
    # splited_value = last_page_onclick_value.split('(')
    # print(splited_value[1][:-1])




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

    for i in range(2, 12):
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
