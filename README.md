# VPN Config Bot

VPN Config Bot — это Telegram-бот для продажи конфигурационных файлов VPN (WireGuard, Outline, Proxy) и создания частных сетей. Бот автоматически выдает файлы пользователю после успешной оплаты.

## Функционал
- Покупка конфигурационных файлов VPN для:
  - WireGuard
  - Outline
  - Proxy
- Автоматическая проверка наличия файлов перед покупкой.
- Отправка конфигурационных файлов после успешной оплаты.
- Создание частной сети (2 файла WireGuard).

## Требования
- Python 3.12
- Установленные зависимости из `requirements.txt`

## Настройка проекта

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Icestorm-dev/vpn1.git
   cd vpn1
   ```

2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте файл `.env`:
   - Впишите токен вашего Telegram-бота:
     ```env
     TELEGRAM_TOKEN=<Ваш токен бота>
     ```

5. Убедитесь, что в папках `vpn/wireguard`, `vpn/outline`, `vpn/proxy` находятся файлы конфигураций (например, `client_1.conf`, `outline_1.txt`, `proxy_1.txt`).

6. Запустите бота:
   ```bash
   python bot.py
   ```

## Команды
- `/start` — Приветственное сообщение и описание функционала.
- `/info` — Информация о боте, ссылки для скачивания приложений.
- `/buy_wireguard` — Купить конфигурацию WireGuard.
- `/buy_outline` — Купить конфигурацию Outline.
- `/buy_proxy` — Купить конфигурацию Proxy.
- `/buy_private_network` — Купить два файла WireGuard для создания частной сети.


