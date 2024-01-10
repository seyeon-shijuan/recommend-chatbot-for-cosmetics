class InferenceResponse():
    def __init__(self, response: str):
        self.response = response

# 클래스 기반 뷰 정의
class InferenceAPIRouter:
    def __init__(self):
        self.items = []

    def create_item(self, item: Item):
        self.items.append(item)
        return item

    def read_item(self, item_id: int):
        if 0 <= item_id < len(self.items):
            return self.items[item_id]
        else:
            return {"error": "Item not found"}