from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from tg_bot.filters.admin_user import IsAdmin
from tg_bot.bot_responses import admin_commands as text
from tg_bot.keyboards.admin_menu import get_setting_buttons


router: Router = Router()
router.message.filter(IsAdmin())

imitation_db = {}  # имитация бд


@router.message(Command(commands=['current_settings']))
async def process_current_settings_cmd(message: Message):
    await message.reply(text.CURRENT_SETTINGS_TEXT, parse_mode='HTML')


@router.message(Command(commands=['deleting_voice']))
async def process_deleting_voice_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Удаление голосовых сообщений:', 
                           reply_markup=reply_markup)


@router.message(Command(commands=['deleting_video']))
async def process_deleting_video_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Удаление видеосообщений:', 
                           reply_markup=reply_markup)


@router.message(Command(commands=['warning_ladder']))
async def process_warning_ladder_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Предупреждение на лесенку\n(лесенка не удаляется):', 
                           reply_markup=reply_markup)


@router.message(Command(commands=['deleting_ladder']))
async def process_deleting_ladder_cmd(message: Message, bot: Bot):
    reply_markup = get_setting_buttons()
    await bot.send_message(chat_id=message.chat.id, 
                           text='Предупреждение на лесенку\n(лесенка удаляется):', 
                           reply_markup=reply_markup)


@router.message(Command(commands=['setting_ladder']))
async def process_setting_ladder_cmd(message: Message):
    await message.reply(text.SETTING_LADDER_TEXT, parse_mode='HTML')


class ChatRules(StatesGroup):
    setting_rules_chat = State()


@router.message(Command('add_chat_rules'))
async def process_add_chat_rules(message: Message, state: FSMContext):
    await message.reply('Отправь ссылку на сообщение с правилами чата.')
    await state.set_state(ChatRules.setting_rules_chat)


@router.message(ChatRules.setting_rules_chat, F.text.regexp(r'\b(http|https):\/\/'))
async def process_setting_rules_chat(message: Message, state: FSMContext):
    link_message = message.text  
    imitation_db['link_message'] = link_message  # пишем в базу
    await message.reply(text.ADD_CHAT_RULES_TEXT, parse_mode='HTML')
    await state.clear()


@router.message(ChatRules.setting_rules_chat)
async def process_setting_rules_chat_incorrectly(message: Message):
    await message.reply(text='Неверный формат, нужно отправить ссылку на сообщение с правилами.')
    