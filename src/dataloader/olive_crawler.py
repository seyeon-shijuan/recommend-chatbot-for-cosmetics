from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from tqdm import tqdm_notebook
# from collections import OrderedDict
import time
# import requests
import pandas as pd
import re
import os

import warnings
warnings.filterwarnings('ignore')


def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

# Selenium Driver에서 Beautiful Soup을 사용해 HTML 가져오기
def get_soup(browser):
    html = browser.page_source
    return BeautifulSoup(html, 'html.parser')


# 페이지의 전체상품 상세링크 가져오기
def get_product_links(soup):
    # class가 "prd_info"인 모든 div 태그를 찾기
    prd_info_divs = soup.find_all('div', class_='prd_info')

    # 결과를 담을 리스트 초기화
    href_list = []

    # 각 div에서 class가 "prd_thumb goodsList"인 모든 a 태그의 href 속성 추출
    for div in prd_info_divs:
        prd_thumb_a = div.find('a', class_='prd_thumb goodsList')
        if prd_thumb_a:
            href = prd_thumb_a.get('href')
            href_list.append(href)

    return href_list


# 페이지별 상품 리뷰 크롤링 함수2
def review_crawling2(browser, category):
    reviews = list()

    # max 페이지
    page_box = browser.find_elements(By.CSS_SELECTOR,'#gdasContentsArea > div > div.pageing > a')
    max_page = len(page_box)

    for page in range(1, max_page):
        if page > 1:
            try:
                browser.find_elements(By.CSS_SELECTOR, '#gdasContentsArea > div > div.pageing > a')[page-2].click()
                time.sleep(2)
            except:
                continue

        for i in range(1, 11):
            soup = get_soup(browser)
            selectors = {
                "brand": f'#Contents > div.prd_detail_box.renew > div.right_area > div > p.prd_name',
                "nickname": f'#gdasList > li:nth-child({i}) > div.info > div > p.info_user > a.id',
                "rate": f'#gdasList > li:nth-child({i}) > div.review_cont > div.score_area > span.review_point > span',
                "skin_type": f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(1) > dd > span',
                "select_1_content": f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(1) > dd > span',
                "select_2_content": f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(2) > dd > span',
                "select_3_content": f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(3) > dd > span',
                "txt": f'#gdasList > li:nth-child({i}) > div.review_cont > div.txt_inner'
            }
            # skin_type이랑 select_1_content랑 동일

            contents = dict()

            for name, selector in selectors.items():
                target_element = soup.select_one(selector)

                # 텍스트 가져오기
                if target_element:
                    text_content = target_element.get_text(strip=True)
                    contents[name] = text_content
                    # print("텍스트:", text_content)
                else:
                    print(f"{name=}-해당하는 요소를 찾을 수 없습니다.")
                    break

            # 제품명 특수문자 제거
            brand_string = contents["brand"]
            brand = re.sub(r'\[.*?\]|\(.*?\)', '', brand_string).strip().replace("  ", " ")
            contents["brand"] = brand
            contents["category"] = category
            try:
                contents["rate"] = contents["rate"][-2]
            except:
                pass

            reviews.append(contents)

    return browser, reviews


# 페이지별 상품 리뷰 크롤링 함수
def review_crawling(df, current_page):
    for i in range(1, 11):  # 한 페이지 내 10개 리뷰 크롤링
        try:
            id = driver.find_element(By.CSS_SELECTOR,
                                     f'#gdasList > li:nth-child({i}) > div.info > div > p.info_user > a.id').text
            category = '스킨/토너'
            brand_string = driver.find_element(By.CSS_SELECTOR,
                                               '#Contents > div.prd_detail_box.renew > div.right_area > div > p.prd_name').text
            brand = re.sub(r'\[.*?\]|\(.*?\)', '', brand_string).strip().replace("  ", " ")
            # if brand_string[0] == '[':
            #     brand_match = re.search(r'\]\s*(.+?)\s*\(', brand_string)
            #     brand = brand_match.group(1)
            #     if brand_string[]
            # else:
            #     brand_match = re.search(r'(.+?)\s*\(', brand_string)
            #     brand = brand_match.group(0)
            # print("매칭되는 부분이 없습니다.")
            rate = driver.find_element(By.CSS_SELECTOR,
                                       f'#gdasList > li:nth-child({i}) > div.review_cont > div.score_area > span.review_point > span').text
            skin_type = driver.find_element(By.CSS_SELECTOR,
                                            f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(1) > dd > span').text
            select_1_content = driver.find_element(By.CSS_SELECTOR,
                                                   f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(1) > dd > span').text
            select_2_content = driver.find_element(By.CSS_SELECTOR,
                                                   f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(2) > dd > span').text
            select_3_content = driver.find_element(By.CSS_SELECTOR,
                                                   f'#gdasList > li:nth-child({i}) > div.review_cont > div.poll_sample > dl:nth-child(3) > dd > span').text
            txt = driver.find_element(By.CSS_SELECTOR,
                                      f'#gdasList > li:nth-child({i}) > div.review_cont > div.txt_inner').text
            df.loc[len(df)] = [id, category, brand, rate, skin_type, select_1_content, select_2_content,
                               select_3_content, txt]
            time.sleep(3)
        except Exception as e:
            print(f"에러 발생: {str(e)}")

    return df


def save_all_products_in_sub_category(name, path):
    # 웹 드라이버 설정
    driver = webdriver.Chrome()
    driver.get(path)

    # 48개씩 보기 클릭
    show48 = "#Contents > div.cate_align_box > div.count_sort.tx_num > ul > li:nth-child(3) > a"
    driver.find_element(By.CSS_SELECTOR, show48).click()

    # 소분류 전체 상품 링크
    # max 페이지
    page_box = driver.find_elements(By.CSS_SELECTOR, '#Container > div.pageing > a')
    max_page = len(page_box)

    sub_category_href_list = list()

    for i in range(1, max_page + 1):
        soup = get_soup(driver)
        href_list = get_product_links(soup)
        sub_category_href_list.extend(href_list)

        # 페이지 이동
        if i == max_page:
            break

        a_index = (i - 1) % 10 + 1
        a_element_xpath = f'//*[@id="Container"]/div[2]/a[{a_index}]'
        driver.find_element(By.XPATH, a_element_xpath).click()

    # csv 저장
    df = pd.DataFrame(sub_category_href_list, columns=['href'])
    file_name = f"data/{name}.csv"
    df.to_csv(file_name, index=False)

    driver.quit()

###########################################################################
'''0. 폴더 생성'''
category_directories = ["./data/skin", "./data/essence", "./data/cream", "./data/lotion", "./data/oil"]
for name in category_directories:
    create_directory(name)

''' 1. 카테고리 별 제품 링크 수집 (카테고리당 최대 480개 씩)
(수집할 링크 목록 모을 때 사용)
'''
# category_dict = {
#     "스킨-토너": "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010013&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010013_MID&trackingCd=Cat100000100010013_MID&t_page=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EA%B4%80&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EC%83%81%EC%84%B8_%EC%A4%91%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_2nd_category_type=%EC%A4%91_%EC%8A%A4%ED%82%A8%2F%ED%86%A0%EB%84%88",
#     "에센스-세럼-앰플": "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010014&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0",
#     "크림": "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010015&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0",
#     "로션": "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010016&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0",
#     "미스트-오일": "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010010&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0"
# }
#
# for name, path in category_dict.items():
#     save_all_products_in_sub_category(name, path)

'''2. 카테고리 제품 정보, 리뷰 데이터 수집'''

# category_names = ["스킨-토너", "에센스-세럼-앰플", "크림", "로션", "미스트-오일"]
# category_path = ["./data/skin", "./data/essence", "./data/cream", "./data/lotion", "./data/oil"]
category_names = ["미스트-오일"]
category_path = ["./data/oil"]
START_IDX = 0

for cat_idx, to_collect in enumerate(category_names):
    sub_category_href_df = pd.read_csv(f"data/{to_collect}.csv")
    sub_category_href_df_start = sub_category_href_df.iloc[START_IDX:, -1]
    sub_category_href_list = list(sub_category_href_df_start)

    # 웹 드라이버 설정
    driver = webdriver.Chrome()

    # 데이터 셋 생성
    review_cols = ['nickname', 'brand', 'category', 'rate', 'skin_type', 'select_1_content', 'select_2_content', 'select_3_content', 'txt']
    df_review_cos1 = pd.DataFrame(columns=review_cols)
    df_ingredient = pd.DataFrame(columns=['name', 'ingredient'])

    # 3. 소분류 제품 수집
    for idx, link in enumerate(sub_category_href_list):
        idx += START_IDX
        driver.get(link)

        # 리뷰 버튼 클릭
        review_button = driver.find_element(By.XPATH, '//*[@id="reviewInfo"]/a')
        review_button.click()
        time.sleep(1)

        # 리뷰 데이터 수집 (제품 1개)
        driver, review_data = review_crawling2(driver, to_collect)
        try:
            tmp = pd.DataFrame(review_data)[review_cols]
            df_review_cos1 = pd.concat([df_review_cos1, tmp], axis=0)
            print(f"{idx=}, {len(df_review_cos1)=}, {df_review_cos1.tail(1)}")
        except Exception as e:
            print("idx: ", idx, e)
            continue

        if len(df_review_cos1) >= 1000:
            filename = f"{category_path[cat_idx]}/{to_collect}-{idx}.csv"
            df_review_cos1.to_csv(filename, index=False)
            df_review_cos1 = pd.DataFrame(columns=review_cols)
            print(f"created: {filename}")

    df_review_cos1.to_csv(f"{category_path[cat_idx]}/{to_collect}-final.csv", index=False)
    df_review_cos1 = pd.DataFrame(columns=review_cols)



# # 전체 페이지 수 설정
# total_pages = 15
#
# # 페이지 번호 초기화
# page_number = 1
#
# while page_number <= 15:  # 페이지 끝 임의로 설정
#     # 현재 페이지의 모든 화장품 이미지 버튼을 클릭
#     for row in range(1, 7):
#         time.sleep(2)
#         for col in range(1, 5):
#             image_button_xpath = f'//*[@id="Contents"]/ul[{row + 1}]/li[{col}]/div/a'
#             image_button = driver.find_element(By.XPATH, image_button_xpath)
#             image_button.click()
#             time.sleep(2)
#
#             # 리뷰 버튼 클릭
#             review_button = driver.find_element(By.XPATH, '//*[@id="reviewInfo"]/a')
#             review_button.click()
#             time.sleep(1)
#
#             # 리뷰 데이터 수집
#             review_data = review_crawling(df_review_cos1, page_number)
#
#             # 리뷰 및 정보 수집
#             # for page_number in range(1, total_pages + 1):
#             #     review_data=review_crawling(df_review_cos1, page_number)
#
#             # # 데이터프레임에 데이터 추가
#             # if review_data is not None:
#             #     df_review_cos1 = df_review_cos1.append(review_data, ignore_index=True)
#             #     page_number += 1
#
#             # 구매 정보 클릭
#             ingredient_button = driver.find_element(By.XPATH, '//*[@id="buyInfo"]')
#             ingredient_button.click()
#             time.sleep(2)
#
#             # 이름, 성분 정보 수집
#             name_string = driver.find_element(By.CSS_SELECTOR,
#                                               '#Contents > div.prd_detail_box.renew > div.right_area > div > p.prd_name').text
#             name = re.sub(r'\[.*?\]|\(.*?\)', '', name_string).strip().replace("  ", " ")
#
#             ingredient = driver.find_element(By.CSS_SELECTOR, '#artcInfo > dl:nth-child(8) > dd').text
#
#             # df_ingredient에 데이터 추가
#             df_to_add = pd.DataFrame({'name': [name], 'ingredient': [ingredient]})
#             df_ingredient = pd.concat([df_ingredient, df_to_add], ignore_index=True)
#
#             # df_review_cos1에 데이터 추가
#             df_review_cos1 = pd.concat([df_review_cos1, review_data], axis=0)
#
#             # 이미지 목록이 있는 페이지로 돌아가기
#             driver.back()
#
#     # 리뷰 csv 파일 저장
#     if df_review_cos1 is not None:
#         df_review_cos1.to_csv(f'./scraping/data/review_data{page_number}.csv', index=False)
#
#     # 페이지 이동 후 로딩을 기다리기 위한 시간 지연
#     time.sleep(2)
#
#     # 10 페이지가 되면 화살표 버튼을 클릭하여 다음 페이지로 이동
#     if page_number % 10 == 0:
#         # arrow_button_xpath = '//*[@id="Container"]/div[2]/a[10]'
#         # driver.find_element(By.XPATH, arrow_button_xpath).click()
#         # time.sleep(2)
#         break
#     else:
#         # 10 페이지가 아니면 a 태그 클릭
#         a_index = (page_number - 1) % 10 + 1
#         a_element_xpath = f'//*[@id="Container"]/div[2]/a[{a_index}]'
#         driver.find_element(By.XPATH, a_element_xpath).click()
#
#     # 페이지 번호 증가
#     page_number += 1
#
# # 성분 csv 파일 저장
# df_ingredient.to_csv(f'./scraping/data/ingredient_data{page_number}.csv', index=False)
#
# # 웹 드라이버 종료
# driver.quit()