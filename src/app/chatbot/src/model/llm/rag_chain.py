from src.model.llm.model_chain import ModelChain
from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_community.vectorstores import Chroma
from fastapi.logger import logger
from typing import Union

class RAGChain(ModelChain):
    
    def __init__(self):
        super().__init__()
        self._is_apply_rag = self._config["RAG-Apply"]
        if self._is_apply_rag:
            self._rag_model_name = self._config["RAG-Id"]
            logger.info(f"RAG: {self._rag_model_name}")
            self._retriever = self._load_retriever()
        
    def _load_retriever(self):
        model_name = self._config["RAG-Id"]
        encode_kwargs = {'normalize_embeddings': True}
        ko_embedding = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs=encode_kwargs
        )

        db = Chroma(persist_directory="resource/data/chroma_db", embedding_function=ko_embedding)
        _retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={'k': 3}
        )
        return _retriever
    
    def ask(self, query: str) -> str:
        prompt_template = """
        ### [INST]
        Instruction: 화장품 정보와 화장품을 사용한 사용자의 리뷰입니다.
        화장품 정보와 리뷰를 참고하여 최대 3개의 상품을 추천하고 추천하는 이유를 답변하세요.
        Here is context to help:

        {context}

        {question}


        ### 답변: [/INST]
        """

        llm = HuggingFacePipeline(pipeline=self._pipe)
        
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_template,
        )
        
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        
        _rag_chain = (
        {"context": self._retriever, "question": RunnablePassthrough()}
            | llm_chain
        )
        
        if not self._is_apply_rag:
            return super().ask(query=query)

        result = _rag_chain.invoke(query) 
        print(f'answer: {result}')
        answer = result['text']
        
        return answer
    
    def _set_metadata():
        metadata_field_info = [
            AttributeInfo(
                name="nickname",
                description="화장품 리뷰 작성자의 닉네임 입니다. 닉네임은 개인정보이므로 사용하면 안됩니다.",
                type="string",
            ),
            AttributeInfo(
                name="제품명",
                description="화장품의 상품명입니다. 화장품 이름을 의미하며 화장품의 용량이 포함되어 있을 수 있습니다.",
                type="string",
            ),
            AttributeInfo(
                name="종류",
                description="화장품 종류를 의미합니다.",
                type="string",
            ),
            AttributeInfo(
                name="평점", 
                description="화장품 사용자의 만족도 입니다. 평점은 1-5 점으로 표현되며 숫자가 높으면 좋은 상품입니다.", 
                type="integer"
            ),
            AttributeInfo(
                name="피부타입", 
                description="화장품이 어떠한 피부타입에 적합한지 의미합니다.", 
                type="string"
            ),
            AttributeInfo(
                name="특징1", 
                description="화장품의 특징입니다.", 
                type="string"
            ),
            AttributeInfo(
                name="특징2", 
                description="화장품의 특징입니다.", 
                type="string"
            ),
            AttributeInfo(
                name="특징3", 
                description="화장품의 특징입니다.", 
                type="string"
            ),
            AttributeInfo(
                name="리뷰", 
                description="화장품 사용자의 후기입니다.", 
                type="string"
            ),
        ]