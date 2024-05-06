from aiogram.utils.markdown import hbold, hcode, hblockquote, hpre

privet = "Hallou, {name}. Time for some fucking magic"

# кнопки
button_menu = "📍Главное меню"
button_admin = "🫠 Админ меню"
button_create_studio = "Добавить студию"
button_delete_studio = "Удалить студию"
button_delete_old_studios = "Удалить старые ключи"
button_key = "Показать ключ"
button_apps = "Приложения"
button_kolya = "Кнопка всевластия"
button_iphone = "У меня айфон"
button_fail = "Не работает"
button_traffic = "Показать трафик"
button_show_log = "Показать лог"
button_key_refresh = "Рефреш ключей"
button_show_studios = "Показать студии"

# тексты сообщений
text_desc = f"Внимательно!\n\nКлюч обновляется каждый календарный месяц 1 числа.\n\n\
Если бот не прислал вам ключ, вам нужно нажать кнопку {hbold(button_key)} и бот пришлёт \
текущий рабочий ключ.\n\nЦифры использованного трафика обновляются в реальном времени.\n\n\
Старые ключи удаляются в {hcode('12:00 МСК')} каждого 2 числа месяца.\n\n\
Если бот не ответил, просто попробуйте ещё раз нажать на кнопку меню через некоторое время \
или отправить произвольное сообщение в чат."
text_apps = f"Самые лучшие вариант приложения в данный момент — гибридный vpn, позволяющий не заходить на российские ресурсы через vpn.\n\n\
То есть, при включённом приложении трафик для инстаграма будет идти через vpn, но при этом яндекс будет открываться с той \
же скоростью, если бы приложение vpn было выключено.\n\n\
Одно из самых удобных приложений — Hiddify. Сразу после открытия приложения первый раз нужно выставить регион Россия и \
всё будет работать автоматически.\n\n\
Свежее приложение можно получить тут: https://github.com/hiddify/hiddify-next/releases\n\n\
Для Windows выбираем {hcode('Setup x64')}, Android — {hcode('APK Universal')} или {hcode('APK ARMv8')}, Mac (макбуки, НЕ айфоны) — {hcode('DMG Universal')}.\n\n\
Как резервное (на случай, если первое не будет работать) ставим приложение Outline:\n\nhttps://play.google.com/store/apps/details?id=org.outline.android.client&hl=ru"
text_iphone = f"1. Устанавливаем https://apps.apple.com/ru/app/streisand/id6450534064\n\
2. Копируем этот текст\n\
{hpre('streisand://aW1wb3J0L3JvdXRlOi8vWW5Cc2FYTjBNRERWQVFJREJBVUdEQjhnSVZWeWRXeGxjMTFrYjIxaGFXNU5ZWFJqYUdWeVZHNWhiV1ZlWkc5dFlXbHVVM1J5WVhSbFozbFVkWFZwWktNSEVSWFVDQWtLQ3d3TkRoQmRaRzl0WVdsdVRXRjBZMmhsY2xaa2IyMWhhVzVTYVhCYmIzVjBZbTkxYm1SVVlXZFdiR2x1WldGeW9LRVBXR2RsYjJsd09uSjFWbVJwY21WamROSVNDUkFUVzI5MWRHSnZkVzVrVkdGbm9SUmVjbVZuWlhod09pNHFYQzV5ZFNUVEZoY0pFQmdaVzI5MWRHSnZkVzVrVkdGblhXUnZiV0ZwYmsxaGRHTm9aWEpXYUhsaWNtbGtwUm9iSEIwZVh4QVFaMlZ2YzJsMFpUcDBaV3hsWjNKaGJWOFFFR2RsYjNOcGRHVTZkMmhoZEhOaGNIQmRaMlZ2YzJsMFpUcGhjSEJzWlY1blpXOXphWFJsT21kdmIyZHNaVjVuWlc5emFYUmxPbWwwZFc1bGMyMEFVZ0JWQUMwQVJBQnBBSElBWlFCakFIVFlQTjMzMkR6ZCtscEpVRTl1UkdWdFlXNWtYeEFrUXpRelFrVTVSRGt0T0RGQk15MDBRamhGTFRrM1JrTXRPRFE0TlVFNFJqZENRelkyQUFnQUV3QVpBQ2NBTEFBN0FFQUFSQUJOQUZzQVlnQmxBSEVBZUFCNUFIc0FoQUNMQUpBQW5BQ2VBSzBBdEFEQUFNNEExUURiQU80QkFRRVBBUjRCTFFGSUFWTUFBQUFBQUFBQ0FRQUFBQUFBQUFBaUFBQUFBQUFBQUFBQUFBQUFBQUFCZWc9PQ==')}\
3. В приложении нажимаем плюс справа вверху и вставляем, сверху появится сообщение, что конфигурация обновлена\n\
4. Копируем ключ и через тот же плюс справа вверху добавляем сервер vpn\n\
5. Как резервное (на случай, если первое не будет работать) ставим приложение Outline и добавляем только ключ:\n\nhttps://apps.apple.com/ru/app/outline-app/id1356177741"
text_fail = "ИДи на хуй, Дима."
text_cancel = "отмена"