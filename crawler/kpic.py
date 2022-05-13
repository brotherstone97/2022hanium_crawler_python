def kpic_total_drug():
    URL = 'https://www.health.kr/searchIdentity/search.asp'
    #약학정보원 의약품 전체 검색
    driver = webdriver.Chrome(executable_path='../chromedriver.exe')
    driver.get(url=URL)

    print(driver.current_url)


    search_button = driver.find_element(By.ID, 'btn_idfysearch')

    search_button.click()