from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db.insert_db import insert_data

def show_detail(driver):
    #original code
    # last_page = get_last_page()

    #test code
    last_page = 1

    # 모든 페이지를 순회하기 위한 반복문. i - 1 = 현재 페이지
    for i in range(last_page):
        # 페이지당 테이블은 하나. 이때 tbody의 xpath
        tbody_xpath = '//*[@id="con_body"]/div[2]/div[3]/div[3]/table/tbody'
        tbody = driver.find_element(By.XPATH, tbody_xpath)

        # tbody에 속한 tr(약물)의 개수
        number_of_row = len(tbody.find_elements(By.TAG_NAME, 'tr'))

        # 조회결과가 없을 때 함수 종료
        if number_of_row == 1:
            return
        print(number_of_row)

        ######테스트용 number_of_row. 후에 삭제 예정
        # number_of_row = 1

        # tr태그(약물) 개수 만큼 반복
        for j in range(1, number_of_row + 1):
            # 약물 상세정보 pop-up의 링크가 담겨있는 a태그(약물이름)

            name = driver.find_element(By.XPATH,f'//*[@id="con_body"]/div[2]/div[3]/div[3]/table/tbody/tr[{j}]/td[2]/span[2]/a')
            popup_URL = name.get_attribute('href')
            print(popup_URL)

            #새탭에 팝업창을 열기 위함.
            script = f"window.open('{popup_URL}')"
            driver.execute_script(script)
            #driver의 target을 새탭으로 전환
            driver.switch_to.window(driver.window_handles[1])

            ######테스트 저장용 dict 후에 DB에 저장예정
            save_tester = {}

            # 이미지 xpath
            image_xpath = ['// *[ @ id = "scroll_01"] / div / div / img',
                           '// *[ @ id = "scroll_01"] / div / div / img[1]']

            # 이미지가 하나일 때와 2개 이상일 때의 xpath가 다르므로 예외처리로 커버해준다. 개수와 상관없이 첫번째 사진을 가져옴
            try:
                image = driver.find_element(By.XPATH, image_xpath[0])
                save_tester['image'] = image.get_attribute('src')
            except:
                image = driver.find_element(By.XPATH, image_xpath[1])
                save_tester['image'] = image.get_attribute('src')

            # 약물 상세정보팝업의 기본정보 테이블의 tr을 순회하기 위한 반복문
            for k in range(1, 5):
                # 약물 기본정보테이블의 titles (제품명, 성상, 모양, 업체명 등)
                title_xpath = f'//*[@id="content"]/section/div[1]/div[2]/table/tbody/tr[{k}]/th'
                # 약물 기본정보테이블의 titles (제품명, 성상, 모양, 업체명 등)에 해당하는 contents (ex:가나릴정, 흰색 원형의 필름코팅정, 영풍제약(주))
                contents_xpath = f'//*[@id="content"]/section/div[1]/div[2]/table/tbody/tr[{k}]/td'
                title = driver.find_element(By.XPATH, title_xpath)
                contents = driver.find_element(By.XPATH, contents_xpath)
                save_tester[title.text] = contents.text

                print('title' + title.text)
                print('contents' + contents.text)
            # 원료약품 및 분량 section의 유효성분 추출
            active_ingredient_xpath = '// *[ @ id = "scroll_02"] / h3[1]'
            # 유효성분의 성분명만 추출
            active_ingredient = driver.find_element(By.XPATH, active_ingredient_xpath).text.split(':')[1].lstrip()
            save_tester['active_ingredient'] = active_ingredient

            # 효능효과
            efficacy_xpath = '// *[ @ id = "_ee_doc"]'
            efficacy = driver.find_element(By.XPATH, efficacy_xpath).text
            save_tester['efficacy'] = efficacy

            # 용법용량
            uses_xpath = '// *[ @ id = "_ud_doc"]'
            uses = driver.find_element(By.XPATH, uses_xpath).text
            save_tester['uses'] = uses

            # 주의사항
            precaution_xpath = '//*[@id="_nb_doc"]'
            precaution = driver.find_element(By.XPATH, precaution_xpath).text
            save_tester['precaution'] = precaution

            # DUR(의약품 적정 사용 정보)
            DUR_thead_xpath = '//*[@id="scroll_06"]/table/thead/tr'
            DUR_thead = driver.find_element(By.XPATH, DUR_thead_xpath)
            number_of_th = len(DUR_thead.find_elements(By.TAG_NAME, 'th'))

            DUR_tbody_xpath = '//*[@id="scroll_06"]/table/tbody'
            DUR_tbody = driver.find_element(By.XPATH, DUR_tbody_xpath)
            number_of_tbody_tr = len(DUR_tbody.find_elements(By.TAG_NAME, 'tr'))
            # number_of_tbody_td = len(DUR_tbody.find_elements(By.TAG_NAME, 'td'))

            print('number_of_tbody_tr: ', number_of_tbody_tr)

            #DUR
            save_tester['DUR'] = []
            # DUR테이블 행 하나당 dict하나로 저장
            for i in range(1, number_of_tbody_tr + 1):
                # DUR테이블의 콘텐츠 tr(행)의 개수에 따라 xpath를 다르게 지정.
                if number_of_tbody_tr <= 1:
                    td_contents_xpath_prefix = f'// *[ @ id = "scroll_06"] / table / tbody / tr /'
                else:
                    td_contents_xpath_prefix = f'// *[ @ id = "scroll_06"] / table / tbody / tr[{i}] /'
                #
                list_element = {}
                #요소로 들어갈 dict의 key로 th태그 text를 사용하기 위한 반복문
                for j in range(1, number_of_th + 1):
                    head_name_xpath = f'// *[ @ id = "scroll_06"] / table / thead / tr / th[{j}]'
                    head_name = driver.find_element(By.XPATH, head_name_xpath).text
                    #dict의 value로 들어갈 td태그의 하위 태그가 없을 경우를 대비한 예외처리
                    try:
                        td_contents_xpath = f'{td_contents_xpath_prefix} td[{j}] / span[2] | {td_contents_xpath_prefix} td[{j}] / a'
                        td_contents = driver.find_element(By.XPATH, td_contents_xpath).text
                        list_element[head_name] = td_contents
                    except:
                        list_element[head_name] = ''
                    print('list_element: ', list_element)
                #한 row가 지나면 dict를 save_tester['DUR]에 append하도록 함
                save_tester['DUR'].append(list_element)
            print(save_tester)
            #크롤링 후 새탭 닫기
            driver.close()
            #db에 저장
            insert_data(save_tester)
            #다시 원래 페이지로 target전환
            driver.switch_to.window(driver.window_handles[0])



# 최대 페이지 정보를 얻기 위함.(onclick attribute의 value이용)
def get_last_page():
    try:
        last_page = driver.find_element(By.CLASS_NAME, 'page_last')
        last_page_onclick_value = last_page.get_attribute('onclick')
        # onclick attribute의 value가 없는 경우 단일페이지이므로 1을 반환
        if not last_page_onclick_value:
            return 1
        print(last_page_onclick_value)

        # value에서 정수만을 추출하기 위함
        splited_value = last_page_onclick_value.split('(')
        print(splited_value[1][:-1])
        # return splited_value
        return 1  # 테스트 용 리턴값 original= splited_value
    except:
        # 항목이 없을 경우
        return 1


# 의약품안전나라 의약품 전체 검색하는 함수
def mfds_total_drug(driver):
    # 의약품안전나라(식약처) URL
    URL = 'https://nedrug.mfds.go.kr/searchDrug'

    driver.get(url=URL)

    print(driver.current_url)

    # 낱알검색 버튼의 xpath
    pill_xpath = '//*[@id="con_body"]/div[2]/div[2]/div[1]/ul/li[2]/a'
    pill_button = driver.find_element(By.XPATH, pill_xpath)

    # 낱알검색 탭 클릭
    pill_button.click()

    # 타입별 데이터 갯수저장할 list (테스트용)
    # number_of_drug_by_type = []

    # 최하단 검색 버튼의 xpath
    search_xpath = '//*[@id="searchGrain"]/fieldset/div[8]/button[1]'
    search = driver.find_element(By.XPATH, search_xpath)

    for i in range(2, 3):  # original stop number-> 12 / tester stop number-> 3
        # 알약 타입 클릭 -> 검색 클릭
        type = driver.find_element(By.XPATH, f'//*[@id="drugShapeList"]/li[{i}]/a')
        type.click()
        # explictly waits 로딩되기 전 먼저 실행되는 걸 방지하기 위함.
        search = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )
        search.click()

        show_detail(driver)
    #     #타입별 갯수(테스트용)
    #     count = driver.find_element(By.XPATH, '//*[@id="con_body"]/div[2]/div[3]/div[2]/p/strong')
    #     number_of_drug_by_type.append(count.text)
    #
    # for i in range(len(number_of_drug_by_type)):
    #     print(f'type{i + 1}의 의약품 갯수: {number_of_drug_by_type[i]}')

    # 약물별 상세정보 팝업의 데이터를 긁어오기 위한 함수
