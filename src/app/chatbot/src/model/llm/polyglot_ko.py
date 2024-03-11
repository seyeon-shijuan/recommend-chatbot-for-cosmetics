import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline, Pipeline
from peft import PeftModel, PeftConfig
from src.model.llm.rag_chain import RAGChain
from fastapi.logger import logger

class PolyglotKo(RAGChain):
    def configure_pipeline(self) -> Pipeline:
        model_id = self._config["Id-Fine-Tuning"]
        config = PeftConfig.from_pretrained(pretrained_model_name_or_path=model_id)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            # bnb_4bit_use_double_quant=True,
            # bnb_4bit_quant_type="nf4",
            # bnb_4bit_compute_dtype=torch.bfloat16
        )
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=config.base_model_name_or_path, 
            quantization_config=bnb_config, device_map={"":0})
        model = PeftModel.from_pretrained(model=model, model_id=model_id)
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_id)
        
        pipe = pipeline(
            model=model,
            tokenizer=tokenizer,
            task="text-generation",
            temperature=0.2,
            return_full_text=True,
            max_new_tokens=512,
        )
        
        return pipe
