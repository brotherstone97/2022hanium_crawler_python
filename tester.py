from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='chromedriver.exe')

URL = 'https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=202105574'

driver.get(url=URL)

# DUR(의약품 적정 사용 정보)
DUR_thead_xpath = '//*[@id="scroll_06"]/table/thead/tr'
DUR_thead = driver.find_element(By.XPATH, DUR_thead_xpath)
number_of_th = len(DUR_thead.find_elements(By.TAG_NAME, 'th'))

DUR_tbody_xpath = '//*[@id="scroll_06"]/table/tbody'
DUR_tbody = driver.find_element(By.XPATH, DUR_tbody_xpath)
number_of_tbody_tr = len(DUR_tbody.find_elements(By.TAG_NAME, 'tr'))
# number_of_tbody_td = len(DUR_tbody.find_elements(By.TAG_NAME, 'td'))

print('number_of_tbody_tr: ', number_of_tbody_tr)

save_tester= {'DUR': []}


# DUR테이블 행 하나당 dict하나로 저장
for i in range(1, number_of_tbody_tr+1):
    # DUR테이블의 콘텐츠 tr(행)의 개수에 따라 xpath를 다르게 지정.
    if number_of_tbody_tr <= 1:
        td_contents_xpath_prefix = f'// *[ @ id = "scroll_06"] / table / tbody / tr /'
    else:
        td_contents_xpath_prefix = f'// *[ @ id = "scroll_06"] / table / tbody / tr[{i}] /'
    #
    list_element = {}
    for j in range(1, number_of_th + 1):
        head_name_xpath = f'// *[ @ id = "scroll_06"] / table / thead / tr / th[{j}]'
        head_name = driver.find_element(By.XPATH, head_name_xpath).text
        try:
            td_contents_xpath = f'{td_contents_xpath_prefix} td[{j}] / span[2] | {td_contents_xpath_prefix} td[{j}] / a'
            td_contents = driver.find_element(By.XPATH, td_contents_xpath).text
            list_element[head_name] = td_contents
        except:
            list_element[head_name] = ''
        print('list_element: ', list_element)
    save_tester['DUR'].append(list_element)
    print(save_tester)
driver.close()
