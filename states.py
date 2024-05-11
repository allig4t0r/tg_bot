from aiogram.fsm.state import State, StatesGroup

class WhereAmI(StatesGroup):
    main_menu_studios = State()
    main_menu_kolya = State()
    main_menu_admin = State()

class AddNewStudio(StatesGroup):
    studio_name = State()
    tg_id = State()

class DeleteStudio(StatesGroup):
    key_id = State()