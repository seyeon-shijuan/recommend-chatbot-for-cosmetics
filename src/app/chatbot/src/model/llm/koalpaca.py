from transformers import AutoModelForCausalLM, pipeline, Pipeline
from peft import PeftModel
from src.model.llm.rag_chain import RAGChain

class KoAlpaca(RAGChain):
    
    def configure_pipeline() -> Pipeline:
        
        model_id = super._config["Id-DPO"]
        based_model_id = super._config["Id-DPO-based"]
        
        base_model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=based_model_id,
            device_map="auto",
            load_in_4bit=True
        )
        model = PeftModel.from_pretrained(model=base_model, model_id=model_id, device_map="auto")
        pipe = pipeline(
            task="text-generation",
            model=model,
            tokenizer=based_model_id,
            do_sample=True,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            return_full_text=False,
            eos_token_id=2,
        )
        
        return pipe
