# google-maps-parser

Проект написан благодаря заказу на фриланс-бирже.
Из названия понятно, что это парсер гугл-карт и сохраняет в MySQL-базу.

Перед запуском должен установлен geckodriver, firefox
Должен создан proxy.txt и добавлять ip-адрес:порт прокси с новой строки.
Далее, надо зайти в config.py с блокнота и отредактировать данные для подключения БД и настройки многопроцессорности.
Теперь можно запускать.
____
При запуске запросит страну и запрос.
Страну писать на русском, а запрос можно на любом языке.
____
Парсер будет информировать какой город он исследовать и о добавлении информации в БД.
