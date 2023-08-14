# Foodgram
Приложение для кулинарных изысков.

## Стек технологий
Python, Django REST API, PostgresQL, Docker, Yandex.Cloud.

## Доступность приложения

ip: 158.160.73.93
superuser: admin;admin
domain: foodgram56.ddns.net

## Установка
Для запуска локально, создайте файл `.env` в родительской директории.

```
Или используйте готовый .env.example подставив там свои данные
```

#### Установка Docker
Выполните
```bash
sudo apt install docker docker-compose
```

### Настройка проекта
1. Запустите docker compose:
```bash
docker-compose up -d
```
2. Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
3. Заполните базу начальными данными (необязательно):
```bash
docker-compose exec backend python manage.py load_data
```
4. Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
5. Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic

docker compose exec backend cp -r /app/static/. /static/static/ 
```