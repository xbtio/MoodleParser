import parse
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '5607982148:AAEQevq5RbiMjfUZFz1vODFg4p2BzlC1_hU'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Mydialog(StatesGroup):
    barcode = State()  # Will be represented in storage as 'Mydialog:otvet'
    pasw = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("команда /parse для парсинга")

@dp.message_handler(commands=['parse'])
async def send_info(message: types.Message):
    await Mydialog.barcode.set()
    await message.reply('Введите баркод')


@dp.message_handler(state=Mydialog.barcode)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['barcode'] = message.text

    await Mydialog.next()
    await message.reply("Введите пароль")

@dp.message_handler(state=Mydialog.pasw)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    await message.reply("Wait a sec")
    async with state.proxy() as data:
        data['pasw'] = message.text
        try:
            values = parse.Parse()
            vv = values.parse(data['barcode'], data['pasw'])
            for q, a in vv.items():
                await bot.send_message(message.chat.id, values.message(q, a))
        except:
            await bot.send_message(message.chat.id, 'бот мертв')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)