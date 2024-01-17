from sympy import Union
from src.model.llm.polyglot_ko import PolyglotKo
from src.model.llm.koalpaca import KoAlpaca
from pydantic import BaseModel
import configparser
from src.api.query_builder import QueryProcessor
from src.api.request import *
    
class PromptResponse(BaseModel):
    state: list[Message]
    answer: str
    products: list
    
class LLMServer():
    
    def __init__(self, query_processor: QueryProcessor):
        
        config = configparser.ConfigParser()
        config.read("config.env")
        model_config = config["model"]
        model_name = model_config["Model-Name"]
        
        self.query_processor = query_processor
        
        self._model = None
        if model_name == "PolyglotKo":
            self._model = PolyglotKo()
        elif model_name == "KoAlpaca":
            self._model = KoAlpaca()
        else:
            raise ValueError(f"모델 이름이 유효하지 않습니다.({model_name})")
        
        # self._model.configure_pipeline()
            
    def inference(self, prompt: Prompt) -> PromptResponse:
        
        query, product_list = self.query_processor.build(prompt)
        answer = self._model.ask(query=query)
        return PromptResponse(state=prompt.get_messages(), answer=answer, products=product_list)
        
query_processor = QueryProcessor()
llm_service = LLMServer(query_processor=query_processor)