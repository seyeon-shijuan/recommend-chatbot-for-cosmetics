from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# WebDriver 초기화
driver = webdriver.Chrome()

# 웹 페이지 열기
driver.get("https://www.glowpick.com/categories/1?ids=1")

# 페이지 로딩을 위해 잠시 기다림
time.sleep(2)

# 검색 결과 출력
ul = driver.find_element(by=By.CSS_SELECTOR, value="ul.contents__ul")
li = ul.find_elements(by=By.CSS_SELECTOR, value="li.contents__ul__li")

for idx in range(len(li)):
    print("--- Next li ---")
    ul = driver.find_element(by=By.CSS_SELECTOR, value="ul.contents__ul")
    li = ul.find_elements(by=By.CSS_SELECTOR, value="li.contents__ul__li")
    time.sleep(0.5)
    driver.execute_script("window.scrollBy(0, 50);")
    time.sleep(0.3)
    li[idx].click()
    # li[idx].send_keys(Keys.ENTER)
    time.sleep(0.3)
    review_items = driver.find_elements(By.CSS_SELECTOR, value="article.review__item")
    print(f"review count: {len(review_items)}")
    for item in review_items:
        print("-------")
        print(item.text)
    driver.back()
    time.sleep(1)

# 브라우저 종료
driver.quit()
