import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

BOT_TOKEN = '8275666105:AAH1c5PxMnOaM_MzEagQ9c241XaJ3Hbc11E'
ADMIN_ID = 5192470703

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

SERVICES = {
    'Разбор натальной карты': 'natal',
    'Расшифровка матрицы судьбы': 'matrix',
    'Расклад на Таро': 'tarot'
}

def get_reply_keyboard():
    buttons = [[KeyboardButton(text=name)] for name in SERVICES.keys()]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=False)

@router.message(Command('start'))
async def send_welcome(message: Message):
    welcome_text = '''⭐ Добро пожаловать в тишину между картами.

Здесь время сплетается в узор, а числа шепчут имена арканов.  
Я — твой проводник в пространстве Матрицы Судьбы и языка Таро.  
Я помогу тебе:  
• 📜 Рассчитать и расшифровать твою персональную Матрицу Судьбы.  
• 🃏 Разложить карты на любой вопрос.  
• 🧭 Увидеть связи между кармическими задачами, дарами и твоим путем.  
• 🪔 Разбор натальной карты.  

Готов(а) сделать первый шаг? Твое путешествие начинается с вопроса, дать рождения... или одной перевернутой карты.'''
    await message.answer(welcome_text, reply_markup=get_reply_keyboard())

@router.message(F.text.in_(SERVICES.keys()))
async def handle_service_selection(message: Message):
    user = message.from_user
    service_name = message.text

    await message.answer('Спасибо за выбор! С вами скоро свяжутся. 🌙')

    username = f'@{user.username}' if user.username else 'нет'
    user_link = f'tg://user?id={user.id}'

    admin_message = f'''🔔 Новый запрос на услугу!

🔹 Услуга: {service_name}
🔹 Пользователь: {user.full_name}
🔹 Username: {username}
🔹 ID: `{user.id}`
🔹 [Открыть чат]({user_link})'''

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode='Markdown')
    except Exception as e:
        print(f'Не удалось отправить админу: {e}')

@router.message()
async def handle_other_messages(message: Message):
    pass

async def main():
    print('Бот запущен...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
