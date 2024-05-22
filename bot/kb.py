from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
      KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import bot.text as text

menu_kolya = [
    [
        KeyboardButton(text=text.button_kolya)
    ]
]

menu_admin = [
    [
        KeyboardButton(text=text.button_studio_create),
        KeyboardButton(text=text.button_studios_show),
        KeyboardButton(text=text.button_studio_delete)
    ],
    [
        KeyboardButton(text=text.button_show_log),
        KeyboardButton(text=text.button_studios_delete_old),
        KeyboardButton(text=text.button_studios_message)
    ],
    [
        KeyboardButton(text=text.button_studios_show_traffic),
        KeyboardButton(text=text.button_studios_renew),
        KeyboardButton(text=text.button_admin_all_keys)
    ]
]

menu_studios = [
    [
        KeyboardButton(text=text.button_key),
        KeyboardButton(text=text.button_apps),
        KeyboardButton(text=text.button_iphone)
    ],
    [
        KeyboardButton(text=text.button_traffic),
        KeyboardButton(text=text.button_fail)
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
