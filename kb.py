from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
      KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import text

menu_kolya = [
    [
        KeyboardButton(text=text.button_kolya)
    ]
]

menu_admin = [
    [
        KeyboardButton(text=text.button_create_studio),
        KeyboardButton(text=text.button_delete_studio),
        KeyboardButton(text=text.button_delete_old_studios)
    ],
    [
        KeyboardButton(text=text.button_show_log),
        KeyboardButton(text=text.button_key_refresh),
        KeyboardButton(text=text.button_show_studios)
    ]
]

menu_studios = [
    [
        KeyboardButton(text=text.button_key),
        KeyboardButton(text=text.button_apps),
        KeyboardButton(text=text.button_iphone)
    ],
    [
        KeyboardButton(text=text.button_traffic)
    ]
]

keyboard_admin = ReplyKeyboardMarkup(
    keyboard=menu_admin,
    resize_keyboard=True
)

keyboard_kolya = ReplyKeyboardMarkup(
    keyboard=menu_kolya,
    resize_keyboard=True,
    input_field_placeholder="НЕ ТРОГАЙ КНОПКУ!!!"
)

keyboard_studios = ReplyKeyboardMarkup(
    keyboard=menu_studios,
    resize_keyboard=True
)
