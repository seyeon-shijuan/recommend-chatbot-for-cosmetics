from langchain_community.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# load the document and split it into chunks
loader = CSVLoader("cosmetic_dataset.csv", csv_args={
  'delimiter': ',',
  'quotechar': '"',
  'fieldnames': ['nickname','제품명','종류','평점','피부타입','특징1','특징2','특징3','리뷰']
})
documents = loader.load()


# VectorDB
model_name = "jhgan/ko-sbert-nli"
encode_kwargs = {'normalize_embeddings': True}
ko_embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)
# save to disk: persist_directory="./chroma_db"
vectorstore = Chroma.from_documents(documents=documents, embedding=ko_embedding, persist_directory="./chroma_db")

# load from disk
# vectorstore = Chroma(persist_directory="./chroma_db", embedding=ko_embedding)

