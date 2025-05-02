
Соберите и запустите:
docker-compose up -d --build

Применение миграций:
docker-compose exec web python manage.py migrate

Создание суперпользователя:
docker-compose exec web python manage.py createsuperuser



