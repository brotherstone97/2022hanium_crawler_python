import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from mfds import mfds_total_drug
# from kpic import kpic_total_drug

#headless 선언
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

path = '/usr/bin/chromedriver'
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)


mfds_total_drug(driver)


driver.close()

# implictly waits
# driver.implicitly_wait(time_to_wait=3)



