from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    db = FAISS.from_texts(
        chunks,
        embedding_model
    )

    return db


def retrieve_context(db, question):

    docs = db.similarity_search(
        question,
        k=3
    )

    return "\n".join(
        doc.page_content
        for doc in docs
    )