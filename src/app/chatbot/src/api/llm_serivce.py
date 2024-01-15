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
    state: list[Message]
    text: str
    
    def __init__(self, **data):
        super().__init__(**data)
        query = Message(role=RoleType.QUESTION, content=self.text)
        self.state.append(query)
        
    def get_messages(self) -> list[Message]:
        return self.state
    
    def to_prompt(self) -> str:
        prompt = reduce(lambda prompt, msg: prompt + msg.to_query(), self.state, "")
        return prompt
    
class PromptResponse(BaseModel):
    state: list[Message]
    answer: str
    
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
            
    def inference(self, prompt: Prompt) -> PromptResponse:
        
        query = prompt.to_prompt()
        answer = self._model.ask(query=query)
        
        return PromptResponse(state=prompt.get_messages(), answer=answer)
        
llm_service = LLMServer()