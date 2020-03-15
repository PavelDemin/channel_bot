from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from app import config

# app_dir: Path = Path(__file__).parent.parent

bot = Bot(config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = RedisStorage2(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB_FSM)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def setup():
    from app.utils import executor
    from app import middlewares
    logger.info("Configure handlers...")
    # noinspection PyUnresolvedReferences
    import app.handlers

    middlewares.setup(dp)
    executor.setup()


