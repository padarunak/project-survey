# Проект опрос

## Что это

Это учебный проект, иллюстрирующий реализацию нескольких типов пользователей. В этом приложении Django модераторы могут создавать опросы, а респонденты могут регистрироваться и проходить опросы по разным категориям.

## Запуск проекта

Первое, склонируйте репозиторий:

```bash
git clone https://github.com/padarunak/project-survey.git
```

Create Virtual Env and Install the requirements:
Создайте venv и установите зависимости:

```bash
cd survey
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

Создайте БД и запустите сервер:

```bash
python manage.py migrate
python manage.py runserver
```

Проект будет доступен по адресу http://127.0.0.1:8000
