  Проект разрабатывается, как платформа для обучения
  ---
**Запуск через Doker:**
+ Клонировать репозиторий
+ Заполнить файл .env-sample и переименовать его в .env
+ Собрать образ и запустить контейнеры в фоновом режиме:
  + docker-compose up -d —build
 ---
**Запуск вручную:**
+ Клонировать репозиторий
+ Заполнить файл .env-sample и переименовать его в .env
+ Установить зависимости
  + poetry install или pip install -r requirements.txt
+ Создть и применить мигации 
  + python manage.py makemigrations
  + python manage.py migrate
+ Заполнить фикстурами(при необходимости), которые лежат в папке fixtures
  + python manage.py loaddata fixtures/lms_data.json
  + python manage.py loaddata fixtures/auth_data.json
  + python manage.py loaddata fixtures/users_data.json
+ Установить дополнительное ПО
  + PostgreSQL
  + Redis
+ Запустить сервис
  + python manage.py runserver
