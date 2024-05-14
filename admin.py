import logging

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import kb
from states import WhereAmI, DeleteStudio, DeleteOldStudios
from db import BotDB
from outline import OutlineServer, OutlineServerErrorException, OutlineLibraryException

logger = logging.getLogger(__name__)

async def create_studio(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    with BotDB() as db, OutlineServer() as outline:
        if not db.get_studio(state_data.get("studio_name")):
            new_key = outline.create_key(name=state_data.get("studio_name"))
            new_studio = db.create_studio(tg_id=state_data.get("studio_tg_id"),
                                          key_id=new_key.key_id,
                                          name=new_key.name,
                                          access_url=new_key.access_url)
            if new_studio:
                await msg.answer("Студия добавлена, Повелитель!",
                                 reply_markup=kb.keyboard_admin)
            else:
                await msg.answer("Студия НЕ добавлена, Повелитель!",
                                 reply_markup=kb.keyboard_admin)
        else:
            await msg.answer(f"Уже есть студия с именем {state_data.get('studio_name')}",
                             reply_markup=kb.keyboard_admin)
    await state.clear()
    await state.set_state(WhereAmI.main_menu_admin)

async def delete_studio(msg: Message, state: FSMContext, old_key_id: int = -1) -> bool:
    current_state = await state.get_state()
    with BotDB() as db, OutlineServer() as outline:
        if current_state == DeleteStudio.key_id:
            state_data = await state.get_data()
            key_id = state_data.get("studio_key_id")
        elif current_state == DeleteOldStudios.confirm and old_key_id != -1:
            key_id = old_key_id
        else:
            await msg.answer(f"Не получилось проверить айди ключа {old_key_id}")
            logger.warn("Something happened when checking key_id")
            return
        try:
            outline.get_key(key_id)
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
        except Exception as e:
            await msg.answer("Непонятная херня")
            logger.exception(f"Nobody knows what happened here, {e}")
        if db.delete_studio(int(key_id)):
            await msg.answer(f"Ключ с key_id {key_id} был успешно удалён в базе, хозяин.",
                             reply_markup=kb.keyboard_admin)
        else:
            await msg.answer(f"Ключа с key_id {key_id} НЕТ в базе, хозяин.",
                             reply_markup=kb.keyboard_admin)
    if current_state == DeleteStudio.key_id:
        await state.clear()
        await state.set_state(WhereAmI.main_menu_admin)