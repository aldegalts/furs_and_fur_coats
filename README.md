# Furs & Fur Coats

REST API интернет‑магазина меховых изделий: каталог, корзина, заказы, аутентификация (пароль и Яндекс OAuth), аналитика и уведомления по email.

## Документация API
Swagger UI: `http://localhost:8000/docs`

## Технологический стек
- FastAPI
- SQLAlchemy 
- Alembic
- PostgreSQL
- Docker, docker‑compose

## Интеграции с внешними сервисами 
- Вход через Яндекс OAuth
- Аналитический эндпоинт с использованием OpenRouter
- Email‑уведомление о заказе (Yandex.SMTP)

## Структура проекта (основное)
```
app/
  errors/          # исключения
  routers/         # эндпоинты FastAPI
  services/        # бизнес-логика (auth, email, orders, ...)
  schemas/         # Pydantic‑схемы запросов/ответов
  utils/
    auth/      # OAuth2/JWT утилиты
    llm/       # OpenRouter клиент
infrastructure/
  database/
    models/        # SQLAlchemy модели
    migrations/    # Alembic миграции
    repository/    # Репозитории для работы с БД
  smtp/            # SMTP‑клиент и шаблоны писем
main.py            # создание FastAPI приложения и роутеров
Dockerfile
docker-compose.yaml
entrypoint.sh
.env.example       
```

## Быстрый старт (Docker)
1) Подготовьте переменные окружения (см. раздел «Переменные окружения»). Удобно создать файл `.env` в корне проекта.
2) Соберите и поднимите контейнеры:
```bash
docker compose up -d --build
```
3) Миграции применяются автоматически при старте `backend` (см. `entrypoint.sh`).
4) API будет доступен на `http://localhost:8000`. Документация Swagger UI: `http://localhost:8000/docs`.

Остановить:
```bash
docker compose down
```

## Локальный запуск без Docker
Требуется Python 3.12+
```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload --port 8000
```
