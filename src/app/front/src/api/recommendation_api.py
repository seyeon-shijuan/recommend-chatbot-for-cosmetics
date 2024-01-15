from abc import ABC, abstractmethod

class RecommendationAPIInterface(ABC):
    
    @abstractmethod
    def search_product_info(self, product_id: int):
        pass
    
class RecommendationAPI(RecommendationAPIInterface):
    
    def search_product_info(self, product_id: int):
        pass