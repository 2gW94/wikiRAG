import os
from pathlib import Path

# Базовые директории
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
LOGS_DIR = BASE_DIR / "logs"

# Создаем необходимые директории
for dir_path in [DATA_DIR, VECTORSTORE_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Параметры
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
BASE_URL = "https://wiki.osdev.org"
OLLAMA_BASE_URL = "http://localhost:11434"