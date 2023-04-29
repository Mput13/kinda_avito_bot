import asyncio
import configparser
import logging
from typing import Union

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import BotCommand

from app.handlers.common import register_handlers_common
from app.handlers.lot_creating import register_handlers_lot_creating
from app.handlers.lot_watching import register_handlers_lot_watching
from app.handlers.user_lot_watching import register_handlers_lot_deleting
from app.handlers.watch_by_category import register_handlers_watch_by_category

logger = logging.getLogger(__name__)


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запуск/перезапск бота"),
        BotCommand(command="/cancel", description="Отменить текущее действие")]
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
    dp.middleware.setup(AlbumMiddleware())
    register_handlers_common(dp)
    register_handlers_lot_creating(dp)
    register_handlers_lot_watching(dp)
    register_handlers_watch_by_category(dp)
    register_handlers_lot_deleting(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
