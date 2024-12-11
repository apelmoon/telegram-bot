import time
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from telegram import Bot

# Ваши Telegram API токен и ID
TOKEN = '8182332127:AAGql7P1lkZb_Z1pNo0KVp__5734D2RcktU'
CHAT_IDS = [421061159, 651133671]  # Список ID для отправки сообщений

# Инициализация бота
bot = Bot(token=TOKEN)

# Множество для хранения уже отправленных ссылок
sent_links = set()

async def send_message(message):
    """Асинхронная функция для отправки сообщения в Telegram."""
    for chat_id in CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            print(f"Сообщение отправлено в Telegram для ID {chat_id}.")  # Сообщение об отладке
        except Exception as e:
            print(f"Ошибка при отправке сообщения для ID {chat_id}: {e}")

async def check_vinted():
    """Асинхронная функция для мониторинга товаров на Vinted."""
    url = 'https://www.vinted.pl/catalog?search_text=Monster%20High&time=1729532789&brand_ids[]=174262&brand_ids[]=263944&brand_ids[]=20485&brand_ids[]=9081&brand_ids[]=350483&brand_ids[]=83598&brand_ids[]=296090&brand_ids[]=288799&brand_ids[]=34&brand_ids[]=499&brand_ids[]=4643873&brand_ids[]=114196&brand_ids[]=3350421&brand_ids[]=265661&order=newest_first&page=1'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Запуск в headless-режиме
        page = await browser.new_page()
        
        while True:
            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_timeout(3000)  # Ожидание 3 секунды для загрузки страницы

                # Получаем HTML-код страницы
                page_content = await page.content()
                soup = BeautifulSoup(page_content, 'html.parser')

                # Поиск элементов с товарами
                items = soup.find_all('div', class_='feed-grid__item-content')
                print(f"Найдено товаров: {len(items)}")  # Сообщение об отладке

                for item in items:
                    price_tag = item.find('p', class_='web_ui__Text__text web_ui__Text__caption web_ui__Text__left web_ui__Text__muted')
                    title_tag = item.find('a', class_='new-item-box__overlay new-item-box__overlay--clickable')
                    if price_tag and title_tag:
                        price_text = price_tag.text.strip().replace('zł', '').replace(',', '.').strip()  # Извлечение цены
                        price = float(price_text)  # Преобразование в число
                        title = title_tag['title'].split(",")[0]  # Извлечение названия товара
                        print(f"Цена товара: {price} zł, Название: {title}")  # Сообщение об отладке

                        if 10 < price <= 75:
                            link = title_tag['href']
                            if link not in sent_links:  # Проверка, была ли ссылка уже отправлена
                                message = f"{title}\nНайден товар по цене {price} zł! Ссылка: {link}"
                                await send_message(message)  # Асинхронная отправка сообщения
                                sent_links.add(link)  # Добавляем ссылку в множество

                await asyncio.sleep(5)  # Пауза между запросами
            except Exception as e:
                print(f"Ошибка: {e}")
                await send_message(f"Ошибка при проверке товаров: {e}")
                await asyncio.sleep(10)  # Пауза перед повторной попыткой

        await browser.close()

async def main():
    await send_message("Бот запущен и начинает проверку товаров на Vinted.")  # Сообщение при запуске бота
    await check_vinted()

# Запуск асинхронного кода
asyncio.run(main())
