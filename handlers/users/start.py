from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
# from states.datacollect import Data
# from aiogram.dispatcher import FSMContext
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters import Text
from loader import dp, bot  # ADMIN_TELEGRAM_ID
# from aiogram.utils.exceptions import ChatNotFound
from keyboards.default.mainbutton import mainbutton

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}! /n", reply_markup=mainbutton )
    
