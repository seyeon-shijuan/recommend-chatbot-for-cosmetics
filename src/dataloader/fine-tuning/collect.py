import configparser
from util import Request, Scrape
from dto import NaverQueryParameter, Naver지식IN

config = configparser.ConfigParser()
config.read("src/dataloader/data_config.env")

naver = config["naver"]
naver_client_id = naver["X-Naver-Client-Id"]
naver_client_secret = naver["X-Naver-Client-Secret"]

request = Request(base_url="https://openapi.naver.com")

headers = {
    "Accept": "application/json",
    "X-Naver-Client-Id": naver_client_id,  # 예시: 인증 토큰 헤더
    "X-Naver-Client-Secret": naver_client_secret,  # 요청 데이터의 타입을 JSON으로 지정하는 헤더
}

query_parameter = NaverQueryParameter(query="화장품")

response = request.get(url=f"/v1/search/kin.json?{query_parameter}", headers=headers)
json = response.json()

naver_in = Naver지식IN(json=json)
# print(naver_in)
count = 0
scrape = Scrape()
for item in naver_in.items:
    soup = scrape.get_html(resource_path=item.link)
    c = soup.select_one("div.checkText") # 
    if c is not None:
        count += 1
print(f"count = {count}")
# soup = scrape.get_html(resource_path=naver_in.items[1].link)
# print(naver_in.items[1].link)
# al = soup.select_one("div._answerList")
# print(al)
# c = soup.select_one("div.checkText") # 
# count = 0
# if c is not None:
#     count += 1
# # print(c.text)
# q = soup.select_one("div.c-heading__content")
# a = soup.select("div.se-main-container")
# # print(q.text)
# # for aaa in a:
# #     print("======답변======")
# #     print(aaa)