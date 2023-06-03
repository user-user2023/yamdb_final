# api_yamdb
![Workflow Status]


### Описание
Это групповой проект. Разработан в учебных целях.
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
### Технологии
Проект написан на python3 на базе django framework со встроенной api документацией Redoc.
Настроена авторизация по коду подтверждения и токену с использованием библиотеки jwt.
Разделение прав доступа через permissions.
Есть возможность фильтрации и поиска данных.
Написана команда import_csv с использованием библиотек csv и sqlite.

### Запуск проекта:

Клонировать репозитория:

```
git clone https://github.com/user-user2023/infra_sp2
```
Запустить Docker

Из папки infra запустить docker-compose.yaml:
```
cd infra_sp2/infra
docker-compose up
```

Команда для пересборки контейнеов:
```
docker-compose up -d --build
```
Применить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input 
```

Проверьте работоспособность приложения:
Перейти на http://localhost/admin/ 

Документация доступна после запуска проекта по адресу
```
http://localhost/redoc/
```
### Примеры запросов в приложении:
#### Регистрация:
```
POST
/api/v1/auth/signup/
data:
{
    "username": "admin2",
    "email": "admin2@mail.ru"
}
Response
{
"email": "string",
"username": "string"
}

```
#### Получение токена:
```
POST
/api/v1/auth/token/
{
    "username": "admin2",
    "confirmation_code": "239123"
}
Response
{
"token": "string"
}
```
#### Произведения:
```
GET
/api/v1/titles/[<title id>/]
Response
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{
"name": "string",
"slug": "string"
}
],
"category": {
"name": "string",
"slug": "string"
}
}

POST
/api/v1/titles/
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
Response

{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
PATCH, DEL
/api/v1/titles/<title id>/
```
#### Категории:
```
GET
/api/v1/categories/
Response
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"name": "string",
"slug": "string"
}
]
}
POST
/api/v1/categories/
{
"name": "string",
"slug": "string"
}
Response
{
"name": "string",
"slug": "string"
}
DEL
/api/v1/categories/<category id>/
```
#### Жанры:
```
GET
/api/v1/genres/
Response
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"name": "string",
"slug": "string"
}
]
}
POST
/api/v1/genres/
{
"name": "string",
"slug": "string"
}
Response
{
"name": "string",
"slug": "string"
}
DEL
/api/v1/genres/<genre id>/
```
#### Ревью:
```
GET
/api/v1/titles/{title_id}/reviews/[<review id/]
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}
]
}

POST
/api/v1/titles/{title_id}/reviews/
{
"text": "string",
"score": 1
}
Response
{
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}
PATCH, DEL
/api/v1/titles/{title_id}/reviews/{review_id}/
```
#### Комментарии:
```
GET
/api/v1/titles/{title_id}/reviews/{review_id}/comments/[<comment id>/]
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
]
}

POST
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
{
"text": "string"
}
Response
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
PATCH, DEL
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```
```
#### Пользователи:
```
GET
/api/v1/users/
Response
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
]
}
POST
/api/v1/users/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
Response
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
Get user by username
GET
/api/v1/users/{username}/
Response
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
PATCH
/api/v1/users/{username}/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
Response
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
DEL
/api/v1/users/{username}/

Get own user data
GET
/api/v1/users/me/
Response
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
PATCH
/api/v1/users/me/
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
Response
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
#### Скрипт import_csv
Умеет читать данные из базы, записывать данные в базу, удалять данные из таблицы.
Скрипт проверяет наличие файла в `api_yamdb/static/data/`.
Прочитать данные из таблицы на основе файла
```
python manage.py import_csv --read category.csv
```
Записать данные в таблицу, на основе файла
```
python manage.py import_csv --write category.csv`
```
Удалить данные из таблицы на основе файла 
```
python manage.py import_csv --delete category.csv
```

### Разработчики:
Анатолий Левченко  
Антон Козлов  
Егор Комелягин  
