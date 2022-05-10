from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='chromedriver.exe')

URL = 'https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=200402915'

driver.get(url=URL)

DUR_tbody_xpath = '//*[@id="scroll_06"]/table/tbody'
DUR_tbody = driver.find_element(By.XPATH, DUR_tbody_xpath)


number_of_tbody_tr = len(DUR_tbody.find_elements(By.TAG_NAME, 'tr'))
number_of_tbody_td = len(DUR_tbody.find_elements(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'td'))
print('number_of_tbody_tr', number_of_tbody_tr)
print('number_of_tbody_td', number_of_tbody_td)


driver.close()
