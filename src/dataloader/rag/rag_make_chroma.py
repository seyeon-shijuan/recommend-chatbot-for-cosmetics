from langchain_community.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# load the document and split it into chunks
def csv_loader(filename, fieldnames):
    loader = CSVLoader(filename, csv_args={
    'delimiter': ',',
    'quotechar': '"',
    'fieldnames': fieldnames
    })
    documents = loader.load()
    return documents
# documents = csv_loader(doc[1], fieldnames[1])

# load embeddings model
def load_embeddings(model_id="jhgan/ko-sbert-nli"):
    model_name = model_id
    encode_kwargs = {'normalize_embeddings': True}
    embedding = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs
    )
    return embedding

# save to disk: persist_directory="./chroma_db"
def init_and_save_vectorstore(documents=csv_loader(), persist_directory="./chroma_db", embedding=load_embeddings()):
    Chroma.from_documents(documents=documents, embedding=embedding, persist_directory=persist_directory)

# load from disk
def load_vectorstore(persist_directory="./chroma_db", embedding=load_embeddings()):
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return vectorstore

def add_vectorstore(vectorstore=load_vectorstore(), documents=csv_loader()) -> None:
    vectorstore.add_texts(texts=[doc.page_content for doc in documents], 
                          metadatas=[doc.metadata for doc in documents])
    vectorstore.persist()


persist_directory = "src/app/chatbot/resource/data/chroma_db"
doc = ['cosmetic_dataset.csv', 'cosmetic_ingredients.csv']
fieldnames = [['nickname','제품명','종류','평점','피부타입','특징1','특징2','특징3','리뷰'], ['성분명','기원 및 정의','배합목적']]


# init and save vectorstore
init_and_save_vectorstore()

# add new vectorstore
documents= csv_loader(doc[1], fieldnames[1])
vectorstore = load_vectorstore()
add_vectorstore(vectorstore=vectorstore, documents=documents)