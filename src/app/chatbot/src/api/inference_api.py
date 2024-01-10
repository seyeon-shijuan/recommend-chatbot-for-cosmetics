class Request():
    
    def __init__(self, query):
        self.query = query

class InferenceResponse():
    
    def __init__(self, response: str):
        self.response = response

class InferenceAPIRouter:

    def inference(self):
        return { "response": "chatbot test" }
    
inferenceAPIRouter = InferenceAPIRouter()