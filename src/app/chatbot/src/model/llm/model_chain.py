from abc import ABC, abstractmethod
from transformers import Pipeline
import configparser
from configparser import ConfigParser

class ModelChain(ABC):
    
    _config: ConfigParser = None
    _pipe: Pipeline = None
    
    def __init__(self):
        self._config = self.configure()
        self._pipe = self.configure_pipeline()
        
    def configure(self) -> ConfigParser :
        config = configparser.ConfigParser()
        config.read("config.env")
        model_config = config["model"]
        return model_config
        
    @abstractmethod
    def configure_pipeline(self) -> Pipeline:
        pass
        
    def ask(self, query: str) -> str:
        
        query = f"{query}\n\n### 답변:"
        ans = self._pipe(query)
        answer = ans[0]["generated_text"]
        
        if "###" in answer:
            answer = answer.split("###")[0]
            print(f'model/llm/model_chain.py log: {answer}')
            
        return answer
        