from src.model.llm.polyglot_ko import PolyglotKo
from enum import Enum
from functools import reduce
from pydantic import BaseModel

class RoleType(Enum):
    QUESTION = "QUESTION"
    ANSWER = "ANSWER"

class Message(BaseModel):
    role: RoleType
    content: str
        
    def to_query(self) -> str:
        return f"### {self.role.value}: {self.content}\n\n"
        
class Prompt(BaseModel):
    messages: list[Message]
    def __init__(self):
        print(f"messages", self.messages)
        
    def add_messages(self, role: RoleType, content: str):
        self.messages.append(Message(role=role, content=content))    
        
    def get_messages(self) -> list[Message]:
        return self.messages
    
    def to_prompt(self) -> str:
        prompt = reduce(lambda prompt, msg: prompt + msg.to_query(), self.messages, "")
        return prompt
        
class LLMService():
    
    def __init__(self, model: PolyglotKo):
        self._model = model
    
    def inference(self, prompt: Prompt):
        
        query = prompt.to_prompt()
        answer = self._model.ask(query=query)
        
        return {
            "answer": answer
        }
        
model_polyglot_ko = PolyglotKo()
model_polyglot_ko.load_model()
llm_service = LLMService(model=model_polyglot_ko)