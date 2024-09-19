# Rental System

Проект Rental System — это веб-приложение на Django для аренды жилья, которое включает функциональность для управления пользователями, бронированиями, объявлениями, отзывами и аналитикой.

## Требования

- Python 3.8+
- Django 3.x+
- MySQL или другая база данных
- Установленный [Graphviz](https://graphviz.org/download/) для генерации диаграмм

## Установка

1. **Клонирование репозитория:**

   ```bash
   git clone https://github.com/username/rental_system.git
   cd rental_system

Создание и активация виртуального окружения:

На Windows:
bash
Копировать код
python -m venv .venv
.venv\Scripts\activate

На MacOS/Linux:
bash
Копировать код
python3 -m venv .venv
source .venv/bin/activate

Установка зависимостей:
Убедитесь, что у вас установлен pip последней версии, затем установите все зависимости:
bash
Копировать код
pip install --upgrade pip
pip install -r requirements.txt

Настройка переменных окружения:
Создайте файл .env в корневой папке проекта и добавьте туда все необходимые переменные окружения. Пример:
env
Копировать код
SECRET_KEY='your_secret_key'
DEBUG=True
DATABASE_NAME='your_database_name'
DATABASE_USER='your_database_user'
DATABASE_PASSWORD='your_database_password'
DATABASE_HOST='localhost'
DATABASE_PORT='3306'
Миграции базы данных:

Миграции базы данных:
Примените все миграции для базы данных:
bash
Копировать код
python manage.py makemigrations
python manage.py migrate

Создание суперпользователя:
Для доступа к панели администратора Django:
bash
Копировать код
python manage.py createsuperuser

Запуск проекта:
Запустите локальный сервер разработки:
bash
Копировать код
python manage.py runserver
Теперь вы можете открыть проект в браузере по адресу: http://127.0.0.1:8000/.

Запуск тестов
Чтобы запустить тесты для проекта, используйте команду:
bash
Копировать код
python manage.py test

Генерация диаграммы моделей
Для генерации схемы базы данных, выполните команду:
bash
Копировать код
python manage.py graph_models -a -o my_project_visualized.png
Убедитесь, что у вас установлен Graphviz и добавлен в PATH.

Основные URL
Админка: http://127.0.0.1:8000/admin/
Swagger-документация: http://127.0.0.1:8000/swagger/
Редок-документация: http://127.0.0.1:8000/redoc/

Описание API
Примеры взаимодействия с API можно найти в Swagger-документации.

Разработка
Коммит изменений:
bash
Копировать код
git add .
git commit -m "Добавил новую функциональность"

Отправка изменений:
bash
Копировать код
git push origin feature/your-feature-name
Создание pull request на GitHub.



