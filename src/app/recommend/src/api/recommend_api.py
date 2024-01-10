class RecommendationResponse():
    
    def __init__(self, response: str):
        self.response = response

class RecommendationAPIRouter:

    def recommend(self):
        return { "response": "recommend test" }
    
recommendationAPIRouter = RecommendationAPIRouter()