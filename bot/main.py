import asyncio
import logging

import src
import keyboards
import aiogram
import sqlite_db
from aiogram import Bot, Dispatcher, F, Router, exceptions
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from enums import BotMessages, Commands, Callbacks, States
from sqlite_db import connect_db

router = Router()

@router.message(Command(commands=[Commands.start.value]))
async def start(msg: Message, state: FSMContext):
    sqlite_db.add_user(id=msg.from_user.id, username=msg.from_user.username)
    await msg.answer(text=f'Hello, {msg.from_user.username}', reply_markup=keyboards.main_menu(owner_id=msg.from_user.id))

@router.callback_query(F.data == Callbacks.add_new_task.value)
async def add_new_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите задачу')
    await state.set_state(States.set_task_name)

@router.message(States.set_task_name)
async def set_task_name(msg: Message, state: FSMContext):
    await state.set_data({'name':msg.text})
    await state.set_state(States.set_task_description)
    await msg.answer(text='Введите описание задачи')

@router.message(States.set_task_description)
async def set_task_description(msg: Message, state: FSMContext):
    data = await state.get_data()
    data['description'] = msg.text
    await state.set_data(data)
async def main():
    global dp, bot
    connect_db()

    bot = Bot(token=src.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.set_my_description(BotMessages.bot_description.value)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())