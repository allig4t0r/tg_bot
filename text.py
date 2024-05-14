from aiogram.utils.markdown import hbold, hcode, hpre

privet = "Hallou, {name}. Time for some fucking magic"

# кнопки
button_menu = "📍Главное меню"
button_admin = "🫠 Админ меню"
button_admin_all_keys = "Ключи без студий"

button_studio_create = "Добавить студию"
button_studio_delete = "Удалить студию"
button_studios_renew = "Renew студий"
button_studios_delete_old = "Удалить _old студии"
button_studios_show = "Показать студии"
button_studios_show_traffic = "Трафик студий"
button_studios_message = "Сообщение студиям"

button_key = "Показать ключ"
button_apps = "Приложения"
button_kolya = "Кнопка всевластия"
button_iphone = "У меня айфон"
button_fail = "Не работает"
button_traffic = "Показать трафик"
button_show_log = "Показать лог"

# тексты сообщений
text_desc = f"Внимательно!\n\nКлюч обновляется каждый календарный месяц 1 числа.\n\n\
Если бот не прислал вам ключ, вам нужно нажать кнопку {hbold(button_key)} и бот пришлёт \
текущий рабочий ключ.\n\nЦифры использованного трафика обновляются в реальном времени.\n\n\
Старые ключи удаляются в {hcode('12:00 МСК')} каждого 2 числа месяца.\n\n\
Если бот не ответил, просто попробуйте ещё раз нажать на кнопку меню через некоторое время \
или отправить произвольное сообщение в чат."
text_apps = f"Самый лучший тип приложений в данный момент — гибридный vpn, позволяющий не заходить на российские ресурсы через vpn.\n\n\
То есть, при включённом приложении трафик для инстаграма будет идти через vpn, но при этом яндекс будет открываться с той \
же скоростью, если бы приложение vpn было выключено.\n\n\
Одно из самых удобных приложений — Hiddify. Сразу после открытия приложения первый раз нужно выставить регион Россия и \
всё будет работать автоматически.\n\n\
Свежее приложение можно получить тут: https://github.com/hiddify/hiddify-next/releases\n\n\
Для Windows выбираем {hcode('Setup x64')}, Android — {hcode('APK Universal')} или {hcode('APK ARMv8')}, Mac (макбуки, НЕ айфоны) — {hcode('DMG Universal')}.\n\n\
Как резервное (на случай, если первое не будет работать) ставим приложение Outline:\n\nhttps://play.google.com/store/apps/details?id=org.outline.android.client&hl=ru"
text_iphone = f"1. Устанавливаем https://apps.apple.com/ru/app/streisand/id6450534064\n\n\
2. Копируем этот текст\n\
{hpre('streisand://aW1wb3J0L3JvdXRlOi8vWW5Cc2FYTjBNRERWQVFJREJBVUdEQjhnSVZWeWRXeGxjMTFrYjIxaGFXNU5ZWFJqYUdWeVZHNWhiV1ZlWkc5dFlXbHVVM1J5WVhSbFozbFVkWFZwWktNSEVSWFVDQWtLQ3d3TkRoQmRaRzl0WVdsdVRXRjBZMmhsY2xaa2IyMWhhVzVTYVhCYmIzVjBZbTkxYm1SVVlXZFdiR2x1WldGeW9LRVBXR2RsYjJsd09uSjFWbVJwY21WamROSVNDUkFUVzI5MWRHSnZkVzVrVkdGbm9SUmVjbVZuWlhod09pNHFYQzV5ZFNUVEZoY0pFQmdaVzI5MWRHSnZkVzVrVkdGblhXUnZiV0ZwYmsxaGRHTm9aWEpXYUhsaWNtbGtwUm9iSEIwZVh4QVFaMlZ2YzJsMFpUcDBaV3hsWjNKaGJWOFFFR2RsYjNOcGRHVTZkMmhoZEhOaGNIQmRaMlZ2YzJsMFpUcGhjSEJzWlY1blpXOXphWFJsT21kdmIyZHNaVjVuWlc5emFYUmxPbWwwZFc1bGMyMEFVZ0JWQUMwQVJBQnBBSElBWlFCakFIVFlQTjMzMkR6ZCtscEpVRTl1UkdWdFlXNWtYeEFrUXpRelFrVTVSRGt0T0RGQk15MDBRamhGTFRrM1JrTXRPRFE0TlVFNFJqZENRelkyQUFnQUV3QVpBQ2NBTEFBN0FFQUFSQUJOQUZzQVlnQmxBSEVBZUFCNUFIc0FoQUNMQUpBQW5BQ2VBSzBBdEFEQUFNNEExUURiQU80QkFRRVBBUjRCTFFGSUFWTUFBQUFBQUFBQ0FRQUFBQUFBQUFBaUFBQUFBQUFBQUFBQUFBQUFBQUFCZWc9PQ==')}\
\n\n3. В приложении нажимаем плюс справа вверху и вставляем, сверху появится сообщение, что конфигурация обновлена\n\n\
4. Копируем ключ и через тот же плюс справа вверху добавляем сервер vpn\n\n\
5. Как резервное (на случай, если первое не будет работать) ставим приложение Outline и добавляем только ключ:\n\nhttps://apps.apple.com/ru/app/outline-app/id1356177741"
text_fail = "0. Убеждаемся, что НЕ используем СТАРЫЙ КЛЮЧ. Удаляем все ключи, которые есть и добавляем только новый, чтобы быть уверенными, что это нужный ключ\n\n\
1. Проверяем вайфай: открываем ya.ru, google.com и убеждаемся, что интернет вообще есть.\n\n\
2. Проверяем впн: открываем приложение впна, включаем и проверяем, что google.com открывается\n\n\
3. Проверяем мобильную связь: отключаем вайфай и остаёмся на мобильном интернете, проверяем работу ya.ru\n\n\
4. Снова проверяем впн как в пункте 2\n\n\
5. Берём ключ и проверяем его же на другом телефоне/компьютере. Если он на другом телефоне работает, что-то случилось с ВАШИМ телефоном\n\n\
6. Если проверяли в Hiddify, попробовать включить впн в Outline. Если проверяли в Outline, попробовать в Hiddify (на компе или андроиде)\n\n\
7. Перезагрузка телефона/компа и сбор ФАКТОВ, что конкретно не работает. Должна быть ошибка подключения где-то в приложении Hiddify или Outline, сделать её скриншот."
text_cancel = "Отмена"
text_no = "Нет"
text_yes = "Да"