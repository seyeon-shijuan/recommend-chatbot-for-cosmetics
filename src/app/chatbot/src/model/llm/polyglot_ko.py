import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline, Pipeline
from peft import PeftModel, PeftConfig
from src.model.llm.rag_chain import RAGChain

class PolyglotKo(RAGChain):
    
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
        
    def configure_pipeline() -> Pipeline:
        model_id = super._config["Id-Fine-Tuning"]
        config = PeftConfig.from_pretrained(model_id)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=config.base_model_name_or_path, 
            quantization_config=bnb_config, device_map={"":0})
        model = PeftModel.from_pretrained(model, model_id)
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        pipe = pipeline(
            model=model,
            tokenizer=tokenizer,
            task="text-generation",
            temperature=0.2,
            return_full_text=True,
            max_new_tokens=1024,
        )
        
        return pipe
