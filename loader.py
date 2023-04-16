from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from language_middleware import setup_middleware


bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Настроим i18n middleware для работы с многоязычностью
i18n = setup_middleware(dp)

# Создадим псевдоним для метода gettext
_ = i18n.gettext