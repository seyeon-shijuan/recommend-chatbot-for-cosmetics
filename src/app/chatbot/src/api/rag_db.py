from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain.schema.runnable import RunnablePassthrough
# # VectorDB
model_name = "jhgan/ko-sbert-nli"
encode_kwargs = {'normalize_embeddings': True}
ko_embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)

# load from disk
db = Chroma(persist_directory="./chroma_db", embedding_function=ko_embedding)
retriever = db.as_retriever(
                            search_type="similarity",
                            search_kwargs={'k': 3}
                        )

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

document_content_description = "화장품의 상세정보와 리뷰 정보"

#### 임시
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig

def load_pipe(model_id="statezeropy/cosmetics-model"):
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
# 서비스 실행에 한번만 실행되어야 한다.
model_id = "statezeropy/cosmetics-model"
pipe = load_pipe(model_id)

prompt_template = """
### [INST]
Instruction: 화장품 정보와 화장품을 사용한 사용자의 리뷰입니다.
화장품 정보와 리뷰를 참고하여 최대 3개의 상품을 추천하고 추천하는 이유를 답변하세요.
반복 답변하지 않습니다.
Here is context to help:

{context}

### 질문: {question}


### 답변: [/INST]
"""

llm = HuggingFacePipeline(pipeline=pipe)
# Create prompt from prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)
# Create llm chain
llm_chain = LLMChain(llm=llm, prompt=prompt)



rag_chain = (
 {"context": retriever, "question": RunnablePassthrough()}
    | llm_chain
)

import warnings
warnings.filterwarnings('ignore')

result = rag_chain.invoke("건성 피부에 좋은 페이셜 크림 추천해줘")

# for i in result['context']:
#     print(f"주어진 근거: {i.page_content} / 출처: {i.metadata['source']} - {i.metadata['page']} \n\n")

print(f"\n답변: {result['text']}")


# split it into chunks
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

# # create the open-source embedding function
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# # load it into Chroma
# db = Chroma.from_documents(docs, embedding_function)

# # query it
# query = "What did the president say about Ketanji Brown Jackson"
# docs = db.similarity_search(query)

# # print results
# print(docs[0].page_content)