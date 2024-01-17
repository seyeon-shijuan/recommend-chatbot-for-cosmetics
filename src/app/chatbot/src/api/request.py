from enum import Enum
from pydantic import BaseModel
from functools import reduce
from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    category: str
    skin_type: str
    contents: list[str]
    image_url: str
    
class RoleType(Enum):
    QUESTION = "질문"
    ANSWER = "답변"
    
class Message(BaseModel):
    role: RoleType
    content: str
        
    def to_query(self) -> str:
        return f"### {self.role.value}: {self.content}\n\n"
        
class Prompt(BaseModel):
    state: list[Message]
    text: str
    product_list: list[str]
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.text:
            self.add_question(self.text)

    def add_question(self, text: str):
        query = Message(role=RoleType.QUESTION, content=text)
        self.state.append(query)

    def get_messages(self) -> list[Message]:
        return self.state

    def to_prompt(self) -> str:
        prompt = reduce(lambda prompt, msg: prompt + msg.to_query(), self.state, "")
        return prompt
