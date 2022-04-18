from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token, owner_id

bot = Bot(token=token, parse_mode='html')
dp = Dispatcher(bot=bot, storage=MemoryStorage())

owner = __import__('asyncio').get_event_loop().run_until_complete(bot.get_chat(owner_id))
