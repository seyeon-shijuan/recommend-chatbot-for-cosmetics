import configparser
from transformers import AutoModelForCausalLM, pipeline
from peft import PeftModel

class Sakura():
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.env")
        model_config = config["model"]
        self.model_id = model_config["Id-DPO"]
        self.based_model_id = model_config["Id-DPO-based"]
        
    def load_model(self):
        base_model = AutoModelForCausalLM.from_pretrained(
            self.based_model_id,
            device_map="auto",
            load_in_4bit=True
        )
        model = PeftModel.from_pretrained(base_model, self.model_id, device_map="auto")
        self.pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=self.based_model_id
        )
        
    def ask(self, query: str) -> str:
        q = f"{query}\n\n### 답변:"
        
        ans = self.pipe(
            q + "\n\n### 답변:",
            do_sample=True,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            return_full_text=False,
            eos_token_id=2,
        )
        
        answer = ans[0]["generated_text"]
        
        if "###" in answer:
            answer = answer.split("###")[0]
            
        return answer