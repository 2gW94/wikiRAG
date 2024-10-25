from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.scraper import OSDevScraper
from src.vectorstore import VectorStoreManager
from src.qa_system import QASystem
from config import BASE_URL, VECTORSTORE_DIR
import uvicorn
from loguru import logger
from pathlib import Path
from typing import Optional, List

app = FastAPI()


class Question(BaseModel):
    text: str


class Answer(BaseModel):
    answer: str
    sources: List[str]
    error: Optional[str] = None


# Глобальные переменные для хранения инстансов
qa_system = None
vector_manager = None


@app.on_event("startup")
async def startup_event():
    global qa_system, vector_manager
    try:
        vector_manager = VectorStoreManager()

        if Path(VECTORSTORE_DIR).exists() and any(Path(VECTORSTORE_DIR).iterdir()):
            logger.info("Loading existing vector store...")
            vectorstore = vector_manager.load_vectorstore()
        else:
            logger.info("Creating new vector store...")
            scraper = OSDevScraper(BASE_URL)
            documents = scraper.scrape("https://wiki.osdev.org/Main_Page", max_pages=50)
            vectorstore = vector_manager.process_and_store(documents)

        qa_system = QASystem(vectorstore)
        logger.info("System initialized successfully")

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise e


@app.post("/query", response_model=Answer)
async def query(question: Question):
    if not qa_system:
        raise HTTPException(status_code=500, detail="System not initialized")

    logger.info(f"Received question: {question.text}")
    try:
        result = qa_system.answer_question(question.text)
        if "error" in result:
            return Answer(answer="", sources=[], error=result["error"])
        return Answer(**result)
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy", "system_ready": qa_system is not None}


if __name__ == "__main__":
    logger.add(
        "logs/main.log",
        rotation="100 MB",
        level="INFO",
        format="{time} {level} {message}"
    )

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise e