# Описание

Данный проект позволяет осуществлять работу с приложением Yatube
по средством API на базе Django + Django REST framework.

# Установка.

## Как запустить проект:

* Клонировать репозиторий и перейти в него в командной строке:

        git clone git@github.com:Fel1-of/api_final_yatube.git
        cd api_final_yatube

* Cоздать и активировать виртуальное окружение:

        python3 -m venv venv
        source venv/Scripts/activate

* Установить зависимости из файла requirements.txt:

        python -m pip install --upgrade pip
        pip install -r requirements.txt

* Выполнить миграции:

        python manage.py migrate
        
* Запустить проект:

        python manage.py runserver

* Перейти на локальный сервер:

        http://127.0.0.1:8000/

# Примеры.

* Примеры запросов можно посмотреть по следующему адресу:

        http://127.0.0.1:8000/redoc/
