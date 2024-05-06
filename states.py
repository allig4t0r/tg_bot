from aiogram.fsm.state import State, StatesGroup

class Whereami(StatesGroup):
    main_menu_studios = State()
    main_menu_kolya = State()
    main_menu_admin = State()
    text_input_studio_name = State()
    text_input_tg_id = State()
    text_input_key_id = State()
    text_input_confirm = State()
