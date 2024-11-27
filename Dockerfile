# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем переменную окружения для Python
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию
WORKDIR /app

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Устанавливаем точку входа
CMD ["python", "main.py"]
