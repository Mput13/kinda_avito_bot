import asyncio
import configparser
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.handlers.common import register_handlers_common
from app.handlers.lot_creating import register_handlers_lot_creating
from app.handlers.lot_watching import register_handlers_lot_watching

logger = logging.getLogger(__name__)


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/create_lot", description="Создать лот")]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    parser = configparser.ConfigParser()
    # Парсинг файла конфигурации
    parser.read("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=parser.get('TG_BOT', 'token'))
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_lot_creating(dp)
    register_handlers_lot_watching(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
