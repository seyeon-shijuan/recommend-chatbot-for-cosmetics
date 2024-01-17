from src.api.llm_serivce import llm_service
from src.api.request import Prompt
import logging

logger = logging.getLogger(__name__)

class Request():
    
    def __init__(self, query):
        self._query = query

class InferenceResponse():
    
    def __init__(self, response: str):
        self.response = response

class ChatbotAPIRouter:
    
    def __init__(self, llm_service):
        self._llm_service = llm_service
        
    def test(self, text):
        logger.debug("sdf")
        return {
            "test": text
        }

    def prompt(self, prompt: Prompt):
        response = self._llm_service.inference(prompt=prompt)
        return response

chatbotAPIRouter = ChatbotAPIRouter(llm_service=llm_service)