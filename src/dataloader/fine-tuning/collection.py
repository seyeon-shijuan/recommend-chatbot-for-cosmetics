import configparser
from util import Request, DateUtil
from dto import NaverQueryParameter, Naver지식IN, FetchType
import pandas as pd
from tqdm import tqdm

class Collection():
    
    def __init__(self, set_filename: str):
        config = configparser.ConfigParser()
        config.read(filenames=set_filename)

        naver = config["naver"]
        naver_client_id = naver["X-Naver-Client-Id"]
        naver_client_secret = naver["X-Naver-Client-Secret"]

        self.request_headers = {
            "Accept": "application/json",
            "X-Naver-Client-Id": naver_client_id,
            "X-Naver-Client-Secret": naver_client_secret,
        }
        
    def collect(self, fetch_type: FetchType, keywords: list[str], instruction: str) -> tuple[pd.DataFrame, str]:
        
        print(f"Fetch Type [{fetch_type.value}]")
    
        request = Request(base_url="https://openapi.naver.com")
        
        naver_in_list = []
        
        columns = ["input", "output"] if fetch_type == FetchType.SINGLE else ["question", "chosen", "rejected"]
        filename = "naver_single_set" if fetch_type == FetchType.SINGLE else "naver_pair_set"
        for keyword in keywords:
            
            print(f"start fetch keyword: {keyword}")
            
            query_parameter = NaverQueryParameter(query=keyword, display=99, start=1)
            response = request.get(url=f"/v1/search/kin.json?{query_parameter}", headers=self.request_headers)
            json = response.json()
            naver_in = Naver지식IN(json=json)
            
            naver_in_list.append(naver_in)

            display_unit_count = 100
            start = 100
            end = 1000
                
            while start <= end:
                query_parameter = NaverQueryParameter(query=keyword, display=display_unit_count, start=start)
                response = request.get(url=f"/v1/search/kin.json?{query_parameter}", headers=self.request_headers)
                json = response.json()
                naver_in = Naver지식IN(json=json)
                naver_in_list.append(naver_in)
                start += display_unit_count
                
            print(f"end fetch")
            
        data = pd.DataFrame(columns=columns)
        
        for naver_in in tqdm(naver_in_list, desc="inprogress"):
            fetch_df = pd.DataFrame(data=naver_in.fetch_item(fetch_type=fetch_type), columns=columns)
            data = pd.concat([data, fetch_df], axis=0, ignore_index=True)
            
        data.insert(loc=0, column="instruction", value=instruction)
        
        save_filename = f"resource/data/{filename}-{DateUtil.get_current_time_form()}"
        
        return data, save_filename
