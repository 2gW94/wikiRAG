from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from loguru import logger
from config import CHUNK_SIZE, CHUNK_OVERLAP, VECTORSTORE_DIR


class VectorStoreManager:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        logger.add(
            "logs/vectorstore.log",
            rotation="100 MB",
            level="INFO",
            format="{time} {level} {message}"
        )

    def process_and_store(self, documents):
        logger.info("Processing documents and creating chunks...")
        texts = []
        metadatas = []

        for doc in documents:
            chunks = self.text_splitter.split_text(doc['content'])
            texts.extend(chunks)
            metadatas.extend([doc['metadata'] for _ in chunks])

        logger.info(f"Created {len(texts)} chunks")

        logger.info("Creating vector store...")
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=str(VECTORSTORE_DIR)
        )
        vectorstore.persist()

        logger.info("Vector store created and persisted")
        return vectorstore

    def load_vectorstore(self):
        logger.info("Loading existing vector store...")
        return Chroma(
            persist_directory=str(VECTORSTORE_DIR),
            embedding_function=self.embeddings
        )