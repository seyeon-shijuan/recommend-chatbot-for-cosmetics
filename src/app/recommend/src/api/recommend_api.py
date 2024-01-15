from src.api.collaboration_filter import CollaborationFilter, collabo_filter
from src.api.product_service import ProductService, product_service

class RecommendationResponse():
    
    def __init__(self, response: str):
        self.response = response

class RecommendationAPIRouter:
    
    def __init__(self, collabo_filter: CollaborationFilter, product_service: ProductService):
        self.collabo_filter = collabo_filter
        self.product_service = product_service
        
    def test(self, text):
        return {
            "test": text
        }

    def recommend_product(self, product_name):
        product_list = self.collabo_filter.get_filter_list(product_name=product_name)
        return { 
            "product_list": product_list 
        }
    
    def product_info(self, product_id):
        product: dict[str, str] = self.product_service.get_product(product_id=product_id)
        return {
            "product": product
        }
    
recommendationAPIRouter = RecommendationAPIRouter(collabo_filter=collabo_filter, product_service=product_service)