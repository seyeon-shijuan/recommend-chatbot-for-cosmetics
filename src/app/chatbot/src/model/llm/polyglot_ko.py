import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
import configparser

class PolyglotKo():
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.env")
        model_config = config["model"]
        self.model_id = model_config["Id-Fine-Tuning"]
    
    def load_model(self):
        config = PeftConfig.from_pretrained(pretrained_model_name_or_path=self.model_id)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=config.base_model_name_or_path, 
            quantization_config=bnb_config, device_map={"":0})
        self._model = PeftModel.from_pretrained(self._model, self.model_id)
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self._model.eval()
        
    def ask(self, query: str) -> str:
        q = f"{query}\n\n### 답변:"
        gened = self._model.generate(
            **self._tokenizer(
                q, 
                return_tensors='pt', 
                return_token_type_ids=False
            ).to('cuda'), 
            max_new_tokens=2048,
            early_stopping=False,
            do_sample=True,
            eos_token_id=2,
            pad_token_id=2,
        )
        tokenized_answer = self._tokenizer.decode(gened[0])
        answer = tokenized_answer.split("### 답변: ")[-1].split("<|endoftext|>")[0]
        return answer