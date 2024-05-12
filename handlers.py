import logging
from hurry.filesize import size
from prettytable import PrettyTable
from typing import Any

from aiogram import Bot, Router, F, flags
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold, hpre, hcode
from aiogram.handlers import ErrorHandler
from aiogram.fsm.context import FSMContext

from outline import OutlineServer
from states import WhereAmI, AddNewStudio, DeleteStudio, DeleteOldStudios, RenewStudios, SendMessageStudios
from db import BotDB
from log import log_tail

import admin
import kb
import text
import users
import config

logger = logging.getLogger(__name__)
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext) -> None:
    await msg.answer(f"Твой ID: {msg.from_user.id}")
    if msg.from_user.id == users.kolya:
        await state.set_state(WhereAmI.main_menu_kolya)
        await msg.answer(f"Добро пожаловать, {hbold('Властелин Студий')}!",)
        await msg.answer_photo(photo=FSInputFile('vlastelin.jpg'),
                               reply_markup=kb.keyboard_kolya)
    # elif msg.from_user.id == users.backup_admin or msg.from_user.id == users.admin:
    elif msg.from_user.id == users.backup_admin:
        await state.set_state(WhereAmI.main_menu_admin)
        await msg.answer(f"Добро пожаловать, {hbold('Властелин')}!",
                         reply_markup=kb.keyboard_admin)
    else:
        with BotDB() as db:
            studio = db.get_studio(msg.from_user.id)
            if studio:
                await state.set_state(WhereAmI.main_menu_studios)
                i = 0
                while (i < len(studio)):
                    await msg.answer(f"Добро пожаловать, {hbold(studio[i][2])}! ✨")
                    i += 1
                await msg.answer(text.text_desc,
                                 reply_markup=kb.keyboard_studios)
            else:
                await msg.answer_sticker(sticker="CAACAgQAAxkBAAEqfYFmAueHoh5q0-m73Nir_Yqm8ZlZ3wACegADJkm4A8VPV5-FVmVTNAQ", 
                                 reply_markup=kb.ReplyKeyboardRemove())

# ================================================================================================
# моё

# ================ ОТМЕНА ЛЮБЫХ КОМАНД

@router.message(AddNewStudio.studio_name, F.text.casefold() == text.text_cancel.casefold())
@router.message(AddNewStudio.tg_id, F.text.casefold() == text.text_cancel.casefold())
@router.message(DeleteStudio.key_id, F.text.casefold() == text.text_cancel.casefold())
@router.message(DeleteOldStudios.confirm, F.text.casefold() == text.text_no.casefold())
@router.message(RenewStudios.confirm, F.text.casefold() == text.text_no.casefold())
@router.message(SendMessageStudios.confirm, F.text.casefold() == text.text_no.casefold())
async def admin_cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    logging.info("STATE: cancelling state %r", current_state)
    await state.clear()
    await state.set_state(WhereAmI.main_menu_admin)
    await message.answer("Галя, у нас отмена!",
                         reply_markup=kb.keyboard_admin)

# ================ ДОБАВЛЕНИЕ НОВОЙ СТУДИИ

@router.message(WhereAmI.main_menu_admin, F.text.casefold() == text.button_studio_create.casefold())
async def admin_create_studio_start(msg: Message, state: FSMContext):
    await state.set_state(AddNewStudio.studio_name)
    await msg.answer("Введите имя студии, Повелитель!",
                     reply_markup=kb.ReplyKeyboardRemove())

@router.message(AddNewStudio.studio_name)
async def admin_input_studio_name(msg: Message, state: FSMContext):
    if msg.text.startswith(config.DB_STUDIO_KEYWORD + ' '):
        await state.update_data(studio_name = msg.text)
        await state.set_state(AddNewStudio.tg_id)
        await msg.answer("Введите tg_id, Повелитель ^^",
                         reply_markup=kb.ReplyKeyboardRemove())
    else:
        await msg.answer("Имя студии должно начинаться с кейворда "
                         f"{hbold(config.DB_STUDIO_KEYWORD)}, Повелитель!",
                         reply_markup=kb.ReplyKeyboardRemove())

@router.message(AddNewStudio.tg_id)
async def admin_input_studio_tg_id(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(studio_tg_id = msg.text)
        await admin.create_studio(msg, state)
    else:
        await msg.answer("Нужно число, Повелитель!",
                         reply_markup=kb.ReplyKeyboardRemove())

# ================ УДАЛЕНИЕ СТУДИИ

@router.message(WhereAmI.main_menu_admin, F.text.casefold() == text.button_studio_delete.casefold())
async def admin_delete_studio_start(msg: Message, state: FSMContext):
    await state.set_state(DeleteStudio.key_id)
    await msg.answer("Укажите key_id нужной студии для удаления, Повелитель.")
    await admin_show_studios(msg, state)

@router.message(DeleteStudio.key_id)
async def admin_input_studio_key_id(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(studio_key_id = msg.text)
        await admin.delete_studio(msg, state)
    else:
        await msg.answer("Нужно число, Повелитель!",
                         reply_markup=kb.ReplyKeyboardRemove())

# ================ ПОКАЗАТЬ СТУДИИ

@router.message(WhereAmI.main_menu_admin, F.text.casefold() == text.button_studios_show.casefold())
async def admin_show_studios(msg: Message, state: FSMContext):
    with BotDB() as db:
        studios = db.get_studios()
        if studios:
            message = '\n'.join(str(s) for s in studios)
            current_state = await state.get_state()
            if current_state == WhereAmI.main_menu_admin:
                await msg.answer(f"{message}",
                                 reply_markup=kb.keyboard_admin)
            elif current_state == DeleteStudio.key_id:
                await msg.answer(f"{message}",
                             reply_markup=kb.ReplyKeyboardRemove())
        else:
            await msg.answer("Студий нет :)",
                             reply_markup=kb.keyboard_admin)

# ================ УДАЛЕНИЕ _OLD КЛЮЧЕЙ

@router.message(WhereAmI.main_menu_admin, F.text.casefold() == text.button_studios_delete_old.casefold())
async def admin_delete_old_studios_start(msg: Message, state: FSMContext):
    await state.set_state(DeleteOldStudios.confirm)
    await msg.answer("Грохаем всё старое к хуям, да? Повелитель.",
                     reply_markup=kb.ReplyKeyboardRemove())

@router.message(DeleteOldStudios.confirm, F.text.casefold() == text.text_yes.casefold())
async def admin_delete_old_studios(msg: Message, state: FSMContext):
    with BotDB() as db:
        studios = db.get_old_studios()
        if studios:
            i = 0
            while (i < len(studios)):
                await msg.answer(f"Нахуй идёт {studios[i][2]}")
                await admin.delete_studio(msg, state, studios[i][1])
                i += 1
        else:
            await msg.answer("Ну и не нужны нам эти ваши студии",
                             reply_markup=kb.keyboard_admin)
    await state.clear()
    await state.set_state(WhereAmI.main_menu_admin)

@router.message(DeleteOldStudios.confirm)
async def admin_delete_old_studios_confirm(msg: Message):
    await msg.answer("Хочу чёткий ответ, без этих соплей")

# ================ ПОСЛАТЬ СТУДИЯМ СООБЩЕНИЕ

@router.message(WhereAmI.main_menu_admin, F.text.casefold() == text.button_studios_message.casefold())
async def admin_send_studios_message_start(msg: Message, state: FSMContext):
    await state.set_state(SendMessageStudios.message)
    await msg.answer(f"Пожалуйста, введите сообщение для всех студий, {hbold('Повелитель')}",
                     reply_markup=kb.ReplyKeyboardRemove())

@router.message(SendMessageStudios.message)
async def admin_send_studios_message_input(msg: Message, state: FSMContext):
    await state.update_data(studio_message = msg.text)
    await msg.answer(f"Такое сообщение будет послано, верно?\n\n{hpre(msg.text)}")
    await state.set_state(SendMessageStudios.confirm)

@router.message(SendMessageStudios.confirm, F.text.casefold() == text.text_yes.casefold())
async def admin_send_studio_message(msg: Message, state: FSMContext):
    await msg.answer("Повелитель! Посылаю сообщения…")
    state_data = await state.get_data()
    with BotDB() as db:
        studios = db.get_all_studios()
        if studios:
            i = 0
            while (i < len(studios)):
                await msg.answer(f"Отправляю в {hcode(studios[i][2])}")
                await bot.send_message(studios[i][0], state_data.get("studio_message"))
                logger.info(f"BOT MESSAGE: sent message to studio {studios[i][2]}")
                i += 1
    await msg.answer(f"{hbold('Готово')}",
                     reply_markup=kb.keyboard_admin)
    await state.clear()
    await state.set_state(WhereAmI.main_menu_admin)

@router.message(SendMessageStudios.confirm)
async def admin_send_studios_message_confirm(msg: Message):
    await msg.answer("Хочу чёткий ответ, без этих соплей")

# ================ ПОКАЗАТЬ ЛОГИ

@router.message(WhereAmI.main_menu_admin, F.text.casefold() == text.button_show_log.casefold())
async def admin_logtail(msg: Message):
    logs = log_tail(config.LOG_LINESNUM)
    message = '\n'.join(str(ll) for ll in logs)
    await msg.answer(f"{message}",
                     reply_markup=kb.keyboard_admin)

# ================ ПОКАЗАТЬ ТРАФИК ВСЕХ СТУДИЙ

@router.message(WhereAmI.main_menu_kolya, F.text.casefold() == text.button_kolya.casefold())
@router.message(WhereAmI.main_menu_admin, F.text.casefold() == text.button_studios_show_traffic.casefold())
async def admin_show_traffic_studios(msg: Message, state: FSMContext):
    await msg.answer("Трафик всех студий")
    traffic_message = await msg.answer("Собираю данные, хозяин…")
    with BotDB() as db, OutlineServer() as outline:
        studios = db.get_studios()
        current_state = await state.get_state()
        if studios:
            i = 0
            table = PrettyTable()
            table.field_names = ["Студия", "Трафик"]
            while (i < len(studios)):
                key = outline.get_key(str(studios[i][1]))
                if key.used_bytes is None:
                    table.add_row([studios[i][2], 'ноль байтиков'])
                else:
                    table.add_row([studios[i][2], size(key.used_bytes)])
                i += 1
            if current_state == WhereAmI.main_menu_admin:
                await traffic_message.edit_text(f"{hcode(table)}")
            elif current_state == WhereAmI.main_menu_kolya:
                await traffic_message.edit_text(f"{hcode(table)}")
        else:
            if current_state == WhereAmI.main_menu_admin:
                await msg.answer("Студий нет :)",
                                 reply_markup=kb.keyboard_admin)
            elif current_state == WhereAmI.main_menu_kolya:
                await msg.answer("Колян!!! Студий не существует 🌚",
                                 reply_markup=kb.keyboard_kolya)

@router.message(WhereAmI.main_menu_admin)
async def admin_handler(msg: Message):
    await msg.answer(f"Жду указаний, {hbold('Повелитель')}",
                     reply_markup=kb.keyboard_admin)

# ================================================================================================
# Колян
@router.message(WhereAmI.main_menu_kolya)
async def kolya_handler(msg: Message):
    await msg.answer("There is no escape",
                     reply_markup=kb.keyboard_kolya)

# ================================================================================================
# студии
@router.message(WhereAmI.main_menu_studios, F.text.casefold() == text.button_key.casefold())
async def studios_show_key(msg: Message):
    with BotDB() as db:
        keys = db.get_key(msg.from_user.id)
        if keys:
            i = 0
            while (i < len(keys)):
                await msg.answer(f"Ключ для {keys[i][1]}:\n\n{hpre(keys[i][2])}")
                i += 1
        else:
            await msg.answer("Ключ не найден",
                     reply_markup=kb.keyboard_studios)

@router.message(WhereAmI.main_menu_studios, F.text.casefold() == text.button_traffic.casefold())
async def studios_show_traffic(msg: Message):
    message = await msg.answer("Подготавливаю данные…")
    with BotDB() as db, OutlineServer() as outline:
        studios = db.get_studio(msg.from_user.id)
        if studios:
            i = 0
            while (i < len(studios)):
                key = outline.get_key(studios[i][1])
                if i == 0:
                    if key.used_bytes is None:
                        await message.edit_text(f"{hbold(studios[i][2])} пока не использовала трафик")
                    else:
                        await message.edit_text(f"{hbold(studios[i][2])} использовала {size(key.used_bytes)}")
                if i >= 1:
                    if key.used_bytes is None:
                        await msg.answer(f"{hbold(studios[i][2])} пока не использовала трафик")
                    else:
                        await msg.answer(f"{hbold(studios[i][2])} использовала {size(key.used_bytes)}")
                i += 1

@router.message(WhereAmI.main_menu_studios, F.text.casefold() == text.button_apps.casefold())
async def studios_show_apps(msg: Message):
    await msg.answer(text.text_apps,
                     reply_markup=kb.keyboard_studios)

@router.message(WhereAmI.main_menu_studios, F.text.casefold() == text.button_iphone.casefold())
async def studios_show_iphone(msg: Message):
    await msg.answer(text.text_iphone,
                     reply_markup=kb.keyboard_studios)

@router.message(WhereAmI.main_menu_studios, F.text.casefold() == text.button_fail.casefold())
async def studios_show_fail(msg: Message):
    await msg.answer(text.text_fail,
                     reply_markup=kb.keyboard_studios)

@router.message(WhereAmI.main_menu_studios)
async def studios_handler(msg: Message):
    await msg.answer("Нажмите кнопку в меню",
                     reply_markup=kb.keyboard_studios)

# await msg.answer_photo(photo="AgACAgIAAxkBAAEqetNmArtAYGmJr2_xYsN7DaoAAWkcBl0AAr_XMRsvBhlIecHp26Eda7wBAAMCAANzAAM0BA")
# @router.message(F.from_user.id.in_(users.studios))

@router.errors()
class MyHandler(ErrorHandler):
    async def error_handler(self) -> Any:
        logger.exception(
            "Unexpected exception %s: %s",
            self.exception_name,
            self.exception_message
        )

