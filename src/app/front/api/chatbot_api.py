from abc import ABC, abstractmethod

class ChatData():
    
    def __init__(self, query):
        self.query = query

class ChatbotAPIInterface(ABC):
    
    @abstractmethod
    def query(self, data: ChatData):
        pass
    
class ChatbotAPIRequest(ChatbotAPIInterface):
    
    # override
    def query(self, data: ChatData):
        pass