# course_work

### Подготовка

Перед стартом проекта создаём .env файл в корне проекта и копируем туда:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=course_work
MONGO_INITDB_ROOT_USERNAME=mongo
MONGO_INITDB_ROOT_PASSWORD=mongo123
SECRET_KEY_AUTH=efewf3@1fwefw!edwgwerg
SECRET_KEY_JWT=21423rEFEWF2e1vDG21

### Запуск

Запуск проекта производится с помощью команды в терминале:
docker compose --env-file .env up --build -d


### Открыть
http://localhost:8000/docs#/
