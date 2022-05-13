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

driver = webdriver.Chrome(executable_path='../chromedriver.exe')

mfds_total_drug(driver)


driver.close()

# implictly waits
# driver.implicitly_wait(time_to_wait=3)


