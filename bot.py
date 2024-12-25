import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import LabeledPrice, PreCheckoutQuery, SuccessfulPayment, FSInputFile, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import F
from dotenv import load_dotenv
import asyncio

# Загрузка токенов из .env файла
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
PROVIDER_TOKEN = os.getenv('PROVIDER_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Папки с конфигурационными файлами для разных категорий
CONFIG_FOLDERS = {
    "wireguard": "vpn/wireguard",
    "outline": "vpn/outline",
    "proxy": "vpn/proxy"
}

# Установка цен для каждой категории файлов
PRICE = {
    "wireguard": [LabeledPrice(label="WireGuard конфигурация", amount=2)],  # Цена: 2 XTR
    "outline": [LabeledPrice(label="Outline конфигурация", amount=3)],  # Цена: 3 XTR
    "proxy": [LabeledPrice(label="Proxy конфигурация", amount=1)],  # Цена: 1 XTR
    "private_network": [LabeledPrice(label="Частная сеть (2 файла)", amount=5)]  # Цена: 5 XTR
}

# URL изображений для категорий файлов
IMAGE_URLS = {
    "wireguard": "https://play-lh.googleusercontent.com/tixGgVipnsaKeGQzykJfgSEhUc_YYMSsr3gwBuPTpXb2F1BKPVzv5OxfCrpS8OAXXh8",
    "outline": "https://img.informer.com/icons_mac/png/128/590/590324.png",
    "proxy": "https://proxyline.net/wp-content/uploads/2019/01/1456424459_1389251308_proxydroid.png",
    "private_network": "https://www.liquidweb.com/wp-content/uploads/2021/11/image2.jpg"
}

# Функция для получения доступных файлов в указанной папке
# Проверяет наличие файлов с указанным расширением
# Возвращает список имен файлов

def get_available_files(folder):
    return [f for f in os.listdir(folder) if f.endswith(('.conf', '.txt'))]

# Обработчик команды /start
# Отправляет приветственное сообщение с описанием команд
@dp.message(Command("start"))
async def start_command(message: types.Message):
    start_text = (
        "Привет! Я бот для покупки конфигурационных файлов.\n"
        "Чтобы начать, выбери нужную команду: \n"
        "- /buy_wireguard - для покупки конфигурации WireGuard\n"
        "- /buy_outline - для покупки конфигурации Outline\n"
        "- /buy_proxy - для покупки конфигурации Proxy\n"
        "- /buy_private_network - для покупки частной сети (2 файла WireGuard).\n"
        "Если у тебя есть вопросы, используй команду /info."
    )
    await message.answer(start_text)

# Обработчик команды /info
# Предоставляет информацию о функциях бота
@dp.message(Command("info"))
async def info_command(message: types.Message):
    info_text = (
        "Я бот для продажи конфигурационных файлов.\n\n"
        "Мои возможности:\n"
        "- Покупка конфигураций для WireGuard, Outline и Proxy\n"
        "- Автоматическая выдача конфигурационного файла после оплаты\n"
        "- Создание частной сети из двух пользователей (WireGuard)\n\n"
        "Ссылки для скачивания приложений:\n"
        "- [WireGuard](https://www.wireguard.com/install/)\n"
        "- [Outline](https://getoutline.org/)\n"
        "- [Proxy клиент](https://www.proxifier.com/)\n\n"
        "Если у тебя есть вопросы, свяжись с поддержкой [@ICE_ST0RM](https://t.me/ICE_ST0RM)."
    )
    await message.answer(info_text)

# Функция для отправки инвойса (счета на оплату)
# Аргументы включают: сообщение, заголовок, описание, полезную нагрузку, цены и URL изображения
async def send_invoice(message, title, description, payload, prices, photo_url):
    await bot.send_invoice(
        message.chat.id,
        title=title,
        description=description,
        payload=payload,
        provider_token=PROVIDER_TOKEN,
        currency="XTR",
        prices=prices,
        start_parameter="vpn-buy",
        photo_url=photo_url,
        photo_size=512,
        photo_width=512,
        photo_height=512
    )

# Обработчик команды /buy_wireguard
# Проверяет доступность файлов и отправляет инвойс на оплату
@dp.message(Command("buy_wireguard"))
async def buy_wireguard(message: types.Message):
    files = get_available_files(CONFIG_FOLDERS["wireguard"])
    if not files:
        await message.answer("К сожалению, файлы WireGuard закончились.")
        return
    await send_invoice(
        message,
        "Покупка WireGuard конфигурации",
        "Вы покупаете файл для WireGuard.",
        "wireguard-payment",
        PRICE["wireguard"],
        IMAGE_URLS["wireguard"]
    )

# Обработчик команды /buy_outline
# Проверяет доступность файлов и отправляет инвойс на оплату
@dp.message(Command("buy_outline"))
async def buy_outline(message: types.Message):
    files = get_available_files(CONFIG_FOLDERS["outline"])
    if not files:
        await message.answer("К сожалению, файлы Outline закончились.")
        return
    await send_invoice(
        message,
        "Покупка Outline конфигурации",
        "Вы покупаете файл для Outline.",
        "outline-payment",
        PRICE["outline"],
        IMAGE_URLS["outline"]
    )

# Обработчик команды /buy_proxy
# Проверяет доступность файлов и отправляет инвойс на оплату
@dp.message(Command("buy_proxy"))
async def buy_proxy(message: types.Message):
    files = get_available_files(CONFIG_FOLDERS["proxy"])
    if not files:
        await message.answer("К сожалению, файлы Proxy закончились.")
        return
    await send_invoice(
        message,
        "Покупка Proxy конфигурации",
        "Вы покупаете файл для Proxy.",
        "proxy-payment",
        PRICE["proxy"],
        IMAGE_URLS["proxy"]
    )

# Обработчик команды /buy_private_network
# Проверяет наличие минимум двух файлов WireGuard и отправляет инвойс
@dp.message(Command("buy_private_network"))
async def buy_private_network(message: types.Message):
    files = get_available_files(CONFIG_FOLDERS["wireguard"])
    if len(files) < 2:
        await message.answer("К сожалению, недостаточно файлов для создания частной сети.")
        return
    await send_invoice(
        message,
        "Покупка частной сети",
        "Вы покупаете два файла для создания частной сети.",
        "private-network-payment",
        PRICE["private_network"],
        IMAGE_URLS["private_network"]
    )

# Обработчик предоплаты (PreCheckoutQuery)
# Уведомляет Telegram, что все проверки пройдены успешно
@dp.pre_checkout_query(F.id)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Обработчик успешной оплаты
# Отправляет файлы пользователю в зависимости от оплаченного товара
@dp.message(F.successful_payment)
async def handle_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload

    if payload == "wireguard-payment":
        folder = CONFIG_FOLDERS["wireguard"]
    elif payload == "outline-payment":
        folder = CONFIG_FOLDERS["outline"]
    elif payload == "proxy-payment":
        folder = CONFIG_FOLDERS["proxy"]
    elif payload == "private-network-payment":
        folder = CONFIG_FOLDERS["wireguard"]
        files = get_available_files(folder)[:2]
        for file in files:
            file_path = os.path.join(folder, file)
            input_file = FSInputFile(file_path)
            await bot.send_document(message.chat.id, document=input_file, caption="Config file")
            os.remove(file_path)
        await message.answer("Файлы успешно отправлены. Спасибо за покупку!")
        return

    files = get_available_files(folder)
    if not files:
        await message.answer("К сожалению, файлы закончились.")
        return

    file_to_send = files[0]
    file_path = os.path.join(folder, file_to_send)
    input_file = FSInputFile(file_path)
    await bot.send_document(message.chat.id, document=input_file, caption="Config file")
    os.remove(file_path)

    await message.answer("Файл успешно отправлен. Спасибо за покупку!")

# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
