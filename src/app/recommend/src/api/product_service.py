class ProductService():
    
    def get_product(self, product_id) -> dict[str, str]:
        description = ""
        # TODO 상품 조회 구현
        return {
            "id": product_id,
            "description": description
        }
        
product_service = ProductService()