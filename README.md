![GitHub top language](https://img.shields.io/github/languages/top/alfa-prime/simple-vk-chat-bot)
![GitHub repo size](https://img.shields.io/github/repo-size/alfa-prime/simple-vk-chat-bot)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/alfa-prime/simple-vk-chat-bot)
![GitHub last commit](https://img.shields.io/github/last-commit/alfa-prime/simple-vk-chat-bot)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

## Описание
ВК-чат-бот для знакомств.  
Бот, основываясь на данных пользователя и заданных в диалоге параметрах, ищет подходящих кандидатов.  
В процессе просмотра полученных результатов существует возможность добавлять кандидатов в "черный" и "белый"
списки (кнопки "Нет" и "Да" соотвественно).  
Кандидаты добавленные в один из списков не будут показанны при следующем поиске.  
Есть возможность просмотреть "белый" список.  
При просмотре "белого" списка дана возможность исключать из него кандидатов.

## Перед запуском бота
1. Для установки зависимостей выполнить команду `pip install -r requirements.txt`
2. Для корректной работы необходимо файл .env_ переименовать в .env
3. Заполнить значения переменных в файле .env согласно их названию (**смотри пункт 4**)
4. [Как настроить группу для бота и получить требуемые значения для настройки приложения](documentation/get_and_set_values.MD)

## Запуск бота
1. Для запуска проекта выполнить команду `python main.py`

## Бот запущен
1. Для начала диалога с ботом отправить ему сообщение **Начать**
![](documentation/img/bot_start.png)
2. Подробности работы бота можно узнать послав ему сообщение **Инфо**
