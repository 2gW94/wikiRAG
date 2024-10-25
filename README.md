# OSDev Wiki RAG System

Система для создания базы знаний на основе OSDev Wiki с использованием RAG (Retrieval-Augmented Generation) подхода. Проект позволяет автоматически собирать информацию с wiki.osdev.org, создавать векторное хранилище и отвечать на вопросы, используя локальную языковую модель через Ollama.

## Особенности

- Автоматический сбор данных с wiki.osdev.org
- Векторное хранилище на основе Chroma DB
- Использование Ollama для локального запуска LLM
- REST API на FastAPI
- Подробное логирование всех процессов
- Сохранение и переиспользование векторного хранилища

## Требования

- Python 3.8+
- [Ollama](https://ollama.ai/)
- Минимум 8GB RAM
- 10GB свободного места на диске

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/osdev-rag.git
cd osdev-rag
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Установите Ollama:
```bash
# для Linux
curl https://ollama.ai/install.sh | sh

# для MacOS
brew install ollama
```

5. Загрузите модель:
```bash
ollama pull llama2
```

## Структура проекта

```
osdev_rag/
├── requirements.txt
├── config.py
├── src/
│   ├── __init__.py
│   ├── scraper.py      # Сбор данных с wiki
│   ├── vectorstore.py  # Управление векторным хранилищем
│   └── qa_system.py    # Система вопросов-ответов
├── data/               # Директория для данных
├── vectorstore/        # Векторное хранилище
├── logs/              # Логи
└── main.py            # Основной файл приложения
```

## Использование

1. Запустите Ollama:
```bash
ollama serve
```

2. Запустите приложение:
```bash
python main.py
```

3. API будет доступно по адресу `http://localhost:8000`

### API Endpoints

#### Проверка здоровья системы
```bash
curl http://localhost:8000/health
```

#### Отправка вопроса
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"text": "How to implement a basic bootloader?"}'
```

Пример ответа:
```json
{
    "answer": "Detailed answer about bootloader implementation...",
    "sources": [
        "https://wiki.osdev.org/page1",
        "https://wiki.osdev.org/page2"
    ]
}
```

## Конфигурация

Основные настройки находятся в файле `config.py`:

- `CHUNK_SIZE`: размер чанков текста (по умолчанию 500)
- `CHUNK_OVERLAP`: перекрытие чанков (по умолчанию 50)
- `BASE_URL`: базовый URL wiki
- `MAX_PAGES`: максимальное количество страниц для сбора (в main.py)

## Логирование

Логи сохраняются в директории `logs/` и разделены по компонентам:
- `scraper.log`: логи сбора данных
- `vectorstore.log`: логи работы с векторным хранилищем
- `qa_system.log`: логи системы вопросов-ответов
- `main.log`: основные логи приложения

## Обновление данных

Для обновления базы знаний:
1. Удалите директорию `vectorstore/`
2. Перезапустите приложение

## Решение проблем

### Проблема: Ollama не отвечает
```bash
# Проверьте статус Ollama
ps aux | grep ollama
# Перезапустите Ollama
ollama serve
```

### Проблема: Нехватка памяти
- Уменьшите `MAX_PAGES` в main.py
- Увеличьте размер SWAP
- Используйте более легкую модель в Ollama

## Производительность

- Первый запуск (сбор данных): 10-15 минут
- Загрузка существующего хранилища: 30-60 секунд
- Ответ на вопрос: 5-15 секунд

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Пушните ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Лицензия

Распространяется под лицензией MIT. См. `LICENSE` для дополнительной информации.



## Благодарности

- [OSDev Wiki](https://wiki.osdev.org/)
- [Ollama](https://ollama.ai/)
- [LangChain](https://github.com/hwchase17/langchain)
- [FastAPI](https://fastapi.tiangolo.com/)
