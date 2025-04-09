
FROM python:3.11

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Установим рабочую директорию внутри контейнера
WORKDIR /app

# Копируем только requirements.txt, чтобы кэшировать зависимость
COPY requirements.txt /app/requirements.txt

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальную часть приложения
COPY backend /app/backend
COPY .env /app/.env

# Убедимся, что файлы и директории правильные
RUN ls /app

# Экспонируем порт, на котором будет работать FastAPI
EXPOSE 8000

# Запускаем сервер FastAPI с использованием Uvicorn
CMD ["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

