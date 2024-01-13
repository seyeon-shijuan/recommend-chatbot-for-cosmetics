from src.api.llm_serivce import LLMService

class Request():
    
    def __init__(self, query):
        self.query = query

class InferenceResponse():
    
    def __init__(self, response: str):
        self.response = response

llm_service = LLMService()

class ChatbotAPIRouter:
    
    def __init__(self, llm_service):
        self.llm_service = llm_service
        
    def test(self, text):
        return {
            "test": text
        }

    def prompt(self, prompt: dict):
        response = self.llm_service.inference(prompt=prompt)
        return response

chatbotAPIRouter = ChatbotAPIRouter(llm_service=llm_service)