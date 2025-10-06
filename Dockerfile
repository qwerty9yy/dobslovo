FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Запуск бота
CMD ["python", "-m", "bot.main"]


#Объяснение:
#Легкий базовый образ Python.
#Устанавливаем зависимости, копируем проект, запускаем бота.
#Минимум слоев — оптимизированный размер образа.