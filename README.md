# VKTINDER
### Для запуска бота необходимо:
1. Установить все сторонние библиотеки из файла ```requirements.txt```
2. Создать базу данных с именем ```VKtinder_db```
3. Создать файл ```.env``` и прописать в него:
```
[VK]
user_id_community = токен группы
access_token_app = токен пользователя 

[DB]
LOGIN = Имя пользователя БД
PASSWORD = Пароль пользователя БД
SERVER = localhost
PORT = 5432
DB_NAME = netology_k
```
4. Добавить бота в группу используя [инструкцию](https://github.com/netology-code/adpy-team-diplom/blob/main/group_settings.md)
### Запуск бота:
Бот запускается через файл ```main.py```