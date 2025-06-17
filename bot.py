import asyncio
from aiogram import Bot, Dispatcher, types, F
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import BOT_TOKEN, CHAT_ID
from scheduler import check_and_congratulate


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def escape_markdown(text: str) -> str:
    # Экранируем основные спецсимволы для parse_mode="Markdown"
    escape_chars = r'\_*[]()'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)


async def start_handler(message: types.Message):
    await message.answer("✅ Бот работает!", parse_mode="Markdown")


dp.message.register(start_handler, F.text == "/start")


async def main():
    scheduler = AsyncIOScheduler()
    loop = asyncio.get_running_loop()

    def job_wrapper():
        # Запускаем корутину в event loop из другого потока
        asyncio.run_coroutine_threadsafe(check_and_congratulate(bot), loop)

    # Запускаем задачу каждый день в 10:55 (или поменяй по своему)
    scheduler.add_job(job_wrapper, CronTrigger(hour=8, minute=15))
    scheduler.start()

    print("✅ Бот запущен. Ждет 10:55 каждый день для поздравлений.")

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\n🛑 Бот остановлен вручную.")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
