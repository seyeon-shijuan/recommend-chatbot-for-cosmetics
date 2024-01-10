from abc import ABC, abstractmethod

class ChatRequest():
    
    def __init__(self, query):
        self.query = query

class ChatbotAPIInterface(ABC):
    
    @abstractmethod
    def query(self, data: ChatRequest):
        pass
    
class ChatbotAPIRequest(ChatbotAPIInterface):
    
    # override
    def query(self, data: ChatRequest):
        pass