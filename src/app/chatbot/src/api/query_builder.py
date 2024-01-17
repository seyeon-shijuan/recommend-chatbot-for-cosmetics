from src.api.request import Prompt
from src.api.response import Product, CollaboFilterResponse
import requests
import configparser
from functools import reduce
import logging

logger = logging.getLogger(__name__)
    
class QueryProcessor():
    
    def __init__(self):
        
        config = configparser.ConfigParser()
        config.read("config.env")
        self.api_recommend = config["API-recommend"]
    
    def build(self, prompt: Prompt) -> tuple[str, CollaboFilterResponse]:    
        
        if prompt.product_list:
            
            product_response = self.request_collabo_filter(prompt.product_list)
            query_list = [ 
                self.product2query(idx=idx+1, product=product) 
                for idx, product in enumerate(product_response.product_list) 
            ]
            
            query = reduce(lambda query, q: query + q, query_list, "")
            query += " 위 내용을 바탕으로 상품 추천 질문에 대한 답변을 해주세요."
            return query, product_response.product_list
        
        else:
            return prompt.to_prompt(), []
        
    def request_collabo_filter(self, product_list: list[Product]) -> CollaboFilterResponse:
        product_string = ",".join(product_list)
        host = self.api_recommend["host"]
        port = self.api_recommend["port"]
        end_point_collabo = self.api_recommend["API-collabo"]
        query_parameter = f"product_name={product_string}"
        url = f"http://{host}:{port}{end_point_collabo}?{query_parameter}"
        response = requests.get(url=url)
        print(f"response: {response.json()}")
        product_response = CollaboFilterResponse(**response.json())
        return product_response


    def product2query(self, idx: int, product: Product) -> str:
        query = f" {idx}번째 추천 상품 {product['name']}는 {product['category']} 카테고리에 속하고, {product['skin_type']}. "
        product_contents = [ f"{content}. " for content in product['contents'] ]
        query += f" 또한 다음과 같은 효과가 있어요. {product_contents}\n\n"
        return query
