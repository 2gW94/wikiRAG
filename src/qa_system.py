from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from loguru import logger


class QASystem:
    def __init__(self, vectorstore):
        self.llm = Ollama(
            model="llama2",
            temperature=0.7,
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True,
        )

        logger.add(
            "logs/qa_system.log",
            rotation="100 MB",
            level="INFO",
            format="{time} {level} {message}"
        )

    def answer_question(self, question: str):
        logger.info(f"Processing question: {question}")
        try:
            result = self.qa_chain.invoke({"query": question})  # Changed from __call__ to invoke
            sources = [doc.metadata["source"] for doc in result["source_documents"]]

            return {
                "answer": result["result"],
                "sources": list(set(sources))
            }
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return {"error": str(e)}