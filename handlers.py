from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from aiogram.handlers import ErrorHandler
from aiogram.fsm.context import FSMContext

from typing import Any
from states import Whereami
from db import BotDB
from log import log_tail
from outline import OutlineServer, OutlineServerErrorException, OutlineLibraryException
from hurry.filesize import size

import kb
import text
import users
import logging
import config

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext) -> None:
    await msg.answer(f"Твой ID: {msg.from_user.id}")
    if msg.from_user.id == users.kolya:
        await state.set_state(Whereami.main_menu_kolya)
        await msg.answer(f"Добро пожаловать, {hbold('Властелин Студий')}!",)
        await msg.answer_photo(photo=FSInputFile('vlastelin.jpg'),
                               reply_markup=kb.keyboard_kolya)
    # elif msg.from_user.id == users.backup_admin or msg.from_user.id == users.admin:
    elif msg.from_user.id == users.backup_admin:
        await state.set_state(Whereami.main_menu_admin)
        await msg.answer(f"Добро пожаловать, {hbold('Властелин')}!",
                         reply_markup=kb.keyboard_admin)
    else:
        with BotDB() as db:
            studio = db.get_studio(msg.from_user.id)
            if studio:
                await state.set_state(Whereami.main_menu_studios)
                i = 0
                while(i < len(studio)):
                    await msg.answer(f"Добро пожаловать, {hbold(studio[i][2])}! ✨")
                    i += 1
                await msg.answer(text.text_desc,
                                 reply_markup=kb.keyboard_studios)
            else:
                await msg.answer_sticker(sticker="CAACAgQAAxkBAAEqfYFmAueHoh5q0-m73Nir_Yqm8ZlZ3wACegADJkm4A8VPV5-FVmVTNAQ", 
                                 reply_markup=kb.ReplyKeyboardRemove())

# моё
@router.message(Whereami.main_menu_admin, F.text.casefold() == text.button_create_studio.casefold())
async def admin_create_studio_start(msg: Message, state: FSMContext):
    await state.set_state(Whereami.text_input_studio_name)
    await msg.answer("Введите имя студии, Повелитель!",
                     reply_markup=kb.ReplyKeyboardRemove())

@router.message(Whereami.text_input_studio_name, F.text.casefold() == text.text_cancel.casefold())
@router.message(Whereami.text_input_tg_id, F.text.casefold() == text.text_cancel.casefold())
@router.message(Whereami.text_input_key_id, F.text.casefold() == text.text_cancel.casefold())
async def admin_cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    logging.info("STATE: cancelling state %r", current_state)
    await state.clear()
    await state.set_state(Whereami.main_menu_admin)
    await message.answer("Галя, у нас отмена!",
                         reply_markup=kb.keyboard_admin)

@router.message(Whereami.text_input_studio_name)
async def admin_input_studio_name(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Whereami.text_input_studio_name:
        if msg.text.startswith(config.DB_STUDIO_KEYWORD):
            await state.update_data(studio_name = msg.text)
            await state.set_state(Whereami.text_input_tg_id)
            await msg.answer("Введите tg_id, Повелитель ^^",
                             reply_markup=kb.ReplyKeyboardRemove())
        else:
            await msg.answer("Имя студии должно начинаться с кейворда "
                             f"{hbold(config.DB_STUDIO_KEYWORD)}, Повелитель!",
                             reply_markup=kb.ReplyKeyboardRemove())
            await state.set_state(Whereami.text_input_studio_name)

@router.message(Whereami.text_input_tg_id)
async def admin_input_studio_tg_id(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(studio_tg_id = msg.text)
        await admin_create_studio_finish(msg, state)
    else:
        await msg.answer("Нужно число, Повелитель!",
                         reply_markup=kb.ReplyKeyboardRemove())
        await state.set_state(Whereami.text_input_tg_id)

async def admin_create_studio_finish(msg: Message, state: FSMContext):
    data = await state.get_data()
    with BotDB() as db, OutlineServer() as outline:
        if not db.get_studio(data.get("studio_name")):
            new_key = outline.create_key(name=data.get("studio_name"))
            new_studio = db.create_studio(tg_id=int(data.get("studio_tg_id")),
                                          key_id=int(new_key.key_id),
                                          name=new_key.name,
                                          access_url=new_key.access_url)
            if new_studio:
                await msg.answer("Студия добавлена, Повелитель!",
                                 reply_markup=kb.keyboard_admin)
            else:
                await msg.answer("Студия НЕ добавлена, Повелитель!",
                                 reply_markup=kb.keyboard_admin)
        else:
            await msg.answer(f"Уже есть студия с именем {data.get('studio_name')}",
                             reply_markup=kb.keyboard_admin)
    await state.clear()
    await state.set_state(Whereami.main_menu_admin)
            
@router.message(Whereami.main_menu_admin, F.text.casefold() == text.button_delete_studio.casefold())
async def admin_delete_studio_start(msg: Message, state: FSMContext):
    await state.set_state(Whereami.text_input_key_id)
    await msg.answer("Укажите key_id нужной студии для удаления, Повелитель.")
    await admin_show_studios(msg, state)

@router.message(Whereami.text_input_key_id)
async def admin_input_studio_key_id(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(studio_key_id = msg.text)
        await admin_delete_studio_finish(msg, state)
    else:
        await msg.answer("Нужно число, Повелитель!",
                         reply_markup=kb.ReplyKeyboardRemove())
        await state.set_state(Whereami.text_input_key_id)

async def admin_delete_studio_finish(msg: Message, state: FSMContext):
    data = await state.get_data()
    with BotDB() as db, OutlineServer() as outline:
        key_id = data.get("studio_key_id")
        try:
            outline.get_key(str(key_id))
            outline.delete_key(key_id)
            await msg.answer(f"Ключ с key_id {key_id} был успешно удалён на сервере, хозяин.",
                             reply_markup=kb.keyboard_admin)
            logger.info(f"OUTLINE: key_id {key_id} was successfully deleted")
        except OutlineServerErrorException as e:
            await msg.answer(f"Ключа с key_id {key_id} НЕТ на сервере, хозяин.",
                             reply_markup=kb.keyboard_admin)
            logger.exception(f"OUTLINE: key_id {key_id} doesn't exist, {e}")
        except OutlineLibraryException as e:
            await msg.answer("Непонятная херня")
            logger.exception(f"OUTLINE: что-то с либой, {e}")
        except:
            await msg.answer("Непонятная херня")
        if db.delete_studio(key_id):
            await msg.answer(f"Ключ с key_id {key_id} был успешно удалён в базе, хозяин.",
                             reply_markup=kb.keyboard_admin)
            logger.info(f"DB: studio with key_id {key_id} was successfully deleted")
        else:
            await msg.answer(f"Ключа с key_id {key_id} НЕТ в базе, хозяин.",
                             reply_markup=kb.keyboard_admin)
            logger.error(f"DB: key_id {key_id} doesn't exist")
    await state.clear()
    await state.set_state(Whereami.main_menu_admin)

@router.message(Whereami.main_menu_admin, F.text.casefold() == text.button_show_studios.casefold())
async def admin_show_studios(msg: Message, state: FSMContext):
    with BotDB() as db:
        studios = db.get_studios()
        if studios:
            message = '\n'.join(str(s) for s in studios)
            current_state = await state.get_state()
            if current_state == Whereami.main_menu_admin:
                await msg.answer(f"{message}",
                                 reply_markup=kb.keyboard_admin)
            elif current_state == Whereami.text_input_key_id:
                await msg.answer(f"{message}",
                             reply_markup=kb.ReplyKeyboardRemove())
        else:
            await msg.answer("Студий нет :)",
                             reply_markup=kb.keyboard_admin)

@router.message(Whereami.main_menu_admin, F.text.casefold() == text.button_show_log.casefold())
async def admin_logtail(msg: Message):
    logs = log_tail(config.LOG_LINESNUM)
    message = '\n'.join(str(l) for l in logs)
    await msg.answer(f"{message}")

@router.message(Whereami.main_menu_admin)
async def admin_handler(msg: Message):
    await msg.answer(f"Жду указаний, {hbold('Повелитель')}",
                     reply_markup=kb.keyboard_admin)

# Колян
@router.message(Whereami.main_menu_kolya, F.text.casefold() == text.button_kolya.casefold())
@router.message(Whereami.main_menu_admin, F.text.casefold() == text.button_traffic.casefold())
async def show_traffic_studios(msg: Message):
    await msg.answer("Трафик всех студий")

@router.message(Whereami.main_menu_kolya)
async def kolya_handler(msg: Message):
    await msg.answer("There is no escape",
                     reply_markup=kb.keyboard_kolya)

# студии
@router.message(Whereami.main_menu_studios, F.text.casefold() == text.button_key.casefold())
async def studios_show_key(msg: Message):
    with BotDB() as db:
        keys = db.get_key(msg.from_user.id)
        if keys:
            i = 0
            while(i < len(keys)):
                await msg.answer(f"Ключ для {keys[i][1]}")
                await msg.answer(keys[i][2])
                i += 1
        else:
            await msg.answer("Ключ не найден",
                     reply_markup=kb.keyboard_studios)

@router.message(Whereami.main_menu_studios, F.text.casefold() == text.button_traffic.casefold())
async def studios_show_traffic(msg: Message):
    with BotDB() as db, OutlineServer() as outline:
        studios = db.get_studio(msg.from_user.id)
        if studios:
            i = 0
            while(i < len(studios)):
                key = outline.get_key(studios[i][1])
                if key.used_bytes is None:
                    await msg.answer(f"{hbold(studios[i][2])} пока не использовала трафик",
                                     reply_markup=kb.keyboard_studios)
                else:
                    await msg.answer(f"{hbold(studios[i][2])} использовала {size(key.used_bytes)}",
                                     reply_markup=kb.keyboard_studios)
                i += 1

@router.message(Whereami.main_menu_studios, F.text.casefold() == text.button_apps.casefold())
async def studios_show_apps(msg: Message):
    await msg.answer(text.text_apps,
                     reply_markup=kb.keyboard_studios)

@router.message(Whereami.main_menu_studios, F.text.casefold() == text.button_iphone.casefold())
async def studios_show_iphone(msg: Message):
    await msg.answer(text.text_iphone,
                     reply_markup=kb.keyboard_studios)

@router.message(Whereami.main_menu_studios)
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