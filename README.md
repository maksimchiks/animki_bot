# animki_bot

Highrise Bot на Python с использованием highrise-bot-sdk.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ВАШ_НИК/animki_bot.git
cd animki_bot
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` с вашими переменными окружения:
```
BEARER_TOKEN=your_token_here
ROOM_ID=your_room_id_here
```

## Запуск

```bash
python bot.py
```

## Деплой на Railway

1. Загрузите код на GitHub
2. Подключите репозиторий к Railway
3. Добавьте переменные окружения в настройках проекта Railway
4. Railway автоматически определит Python и запустит `bot.py`
