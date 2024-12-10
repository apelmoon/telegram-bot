# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем необходимые библиотеки для Playwright
RUN apt-get update && apt-get install -y \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libavif15 \
    libenchant2-2 \
    libsecret-1-0 \
    libmanette0.2 \
    libgles2 \
    && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Playwright и скачиваем браузеры
RUN pip install playwright
RUN playwright install

# Копируем код Python в контейнер
COPY telegram_bot.py .

# Команда для запуска бота
CMD ["python", "telegram_bot.py"]
