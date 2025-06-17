import pandas as pd
from datetime import datetime
from aiogram import Bot
from config import CHAT_ID, BOT_TOKEN


def escape_markdown(text: str) -> str:
    # Экранирует спецсимволы Markdown в тексте
    escape_chars = r'\_*[]()'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

async def check_and_congratulate(bot: Bot):
    print("🕘 Проверка на день рождения запущена")
    try:
        df = pd.read_csv("birthday_list.csv")
        today = datetime.today().strftime("%d.%m.%Y")
        birthday_people = df[df['birthday'] == today]

        if birthday_people.empty:
            await bot.send_message(chat_id=bot.chat_id if hasattr(bot, 'chat_id') else None, text="Сегодня нет именинников.")
            print("📭 Никого не поздравляем.")
            return

        messages = []

        for _, row in birthday_people.iterrows():
            name = row.get("name", "").strip()
            username = row.get("username", "").strip()
            phone = row.get("phone", "").strip()
            user_id = str(row.get("user_id", "")).strip()

            parts = []
            if username and username != "-":
                parts.append(username)
            if phone and phone != "-":
                parts.append(f"📱 {phone}")
            if user_id and user_id != "-":
                parts.append(f"🆔 {user_id}")

            if parts:
                # Экранируем name и parts для Markdown
                escaped_name = escape_markdown(name)
                escaped_parts = [escape_markdown(p) for p in parts]
                message = f"🎉 Сегодня день рождения у {escaped_name}: " + " | ".join(escaped_parts)
                messages.append(message)

        if messages:
            full_message = "\n\n".join(messages)
            await bot.send_message(chat_id=bot.chat_id if hasattr(bot, 'chat_id') else None, text=full_message, parse_mode="Markdown")
            print("✅ Сообщение отправлено:")
            print(full_message)
        else:
            await bot.send_message(chat_id=bot.chat_id if hasattr(bot, 'chat_id') else None, text="🎉 Сегодня есть именинники, но без контактных данных.")
            print("⚠ Данные есть, но нет контактов.")

    except Exception as e:
        print(f"❌ Ошибка в check_and_congratulate: {e}")
