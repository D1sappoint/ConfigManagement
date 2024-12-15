# 1 - Клонирование репозитория
Склонируйте репозиторий с исходным кодом и тестами:

git clone <URL репозитория>
cd <директория проекта/homework_3>

# 2 - Установка зависимостей и запуске
unittest

## Запуск
python translator.py --input model_params.conf
python translator.py --input web_server.conf

# 3 - Структура проекта
Проект содержит следующие файлы и директории, связанные с тестированием:
-  model_params.conf
-  web_server.conf
-  evaluator.py
-  lexer.py
-  parser.py
-  test_translator.py
-  translator.py

# 4 - Запуск тестов
python test_translator.py
