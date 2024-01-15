import configparser
from src.model.llm.polyglot_ko import PolyglotKo
from src.model.llm.sakura import Sakura
from enum import Enum
from functools import reduce
from pydantic import BaseModel
import configparser

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
        
    def add_messages(self, role: RoleType, content: str):
        self.messages.append(Message(role=role, content=content))    
        
    def get_messages(self) -> list[Message]:
        return self.messages
    
    def to_prompt(self) -> str:
        prompt = reduce(lambda prompt, msg: prompt + msg.to_query(), self.messages, "")
        return prompt
    
class PromptResponse(BaseModel):
    state: list[Message]
    answer: str
    
    def __init__(self, state: list[Message], answer: str):
        self.state = state
        self.answer = answer
        
class LLMServer():
    
    def __init__(self):
        
        config = configparser.ConfigParser()
        config.read("config.env")
        model_config = config["model"]
        model_name = model_config["Model-Name"]
        
        self._model = None
        if model_name == "PolyglotKo":
            self._model = PolyglotKo()
        elif model_name == "Sakura":
            self._model = Sakura()
        else:
            raise ValueError(f"모델 이름이 유효하지 않습니다.({model_name})")
        
        self._model.load_model()
            
    def inference(self, prompt: Prompt):
        
        query = prompt.to_prompt()
        answer = self._model.ask(query=query)
        
        return PromptResponse(state=prompt.get_messages(), answer=answer)
        
llm_service = LLMServer()