import configparser
from util import Request
from dto import NaverQueryParameter, Naver지식IN, FetchType
import pandas as pd
from tqdm import tqdm

config = configparser.ConfigParser()
config.read("src/dataloader/data_config.env")

naver = config["naver"]
naver_client_id = naver["X-Naver-Client-Id"]
naver_client_secret = naver["X-Naver-Client-Secret"]

request = Request(base_url="https://openapi.naver.com")

headers = {
    "Accept": "application/json",
    "X-Naver-Client-Id": naver_client_id,
    "X-Naver-Client-Secret": naver_client_secret,
}

naver_in_list = []

keywords = [
    "지성 추천",
    "건성 추천",
    "복합성 추천",
    "화장품 트러블",
    "화장품 부작용"
]

for keyword in keywords:
    
    print(f"start fetch keyword: {keyword}")
    
    query_parameter = NaverQueryParameter(query=keyword, display=99, start=1)
    response = request.get(url=f"/v1/search/kin.json?{query_parameter}", headers=headers)
    json = response.json()
    naver_in = Naver지식IN(json=json)
    
    naver_in_list.append(naver_in)

    display_unit_count = 100
    start = 100
    end = 1000
        
    while start <= end:
        query_parameter = NaverQueryParameter(query=keyword, display=display_unit_count, start=start)
        response = request.get(url=f"/v1/search/kin.json?{query_parameter}", headers=headers)
        json = response.json()
        naver_in = Naver지식IN(json=json)
        naver_in_list.append(naver_in)
        start += display_unit_count
        
    print(f"end fetch")
    
data = pd.DataFrame(columns=["instruction", "output"])

for naver_in in tqdm(naver_in_list, desc="inprogress"):
    fetch_df = pd.DataFrame(data=naver_in.fetch_item(fetch_type=FetchType.SINGLE), columns=["instruction", "output"])
    pd.concat([data, fetch_df], axis=0, ignore_index=True)
    
data.to_csv('naver.csv', index=False)

print(len(data))
print(data.head())
