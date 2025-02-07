# WalletAPI Service
Сервис для управления транзакциями и аккаунтами пользователей.

## Тестовые данные
User:
```json
{
  "email": "ben@gmail.com",
  "password": "123"
}
```
Admin:
```json
{
  "email": "john@gmail.com",
  "password": "123"
}
```
Скрипт для получения подписи (Пример):
```sh
  python .\check_signature.py --account_id 3fa85f64-5717-4562-b3fc-2c963f66afa6 --amount 10.0 --transaction_id 3fa85f64-5717-4562-b3fc-2c963f66afa6 --user_id 3fa85f64-5717-4562-b3fc-2c963f66afa6
```
## Запуск проекта
### Локально (Иметь установленный PostgreSQL, либо запущенный в Docker)
1. Создать .env файл и вставить в него значения из ```./.env.example```.
2. Перейти в директорию с приложением:
   ```sh
   cd ./src
3. Применить миграции:
   ```sh
   alembic upgrade head
5. Запустить сервис:
   ```sh
   python ./main.py
### Docker
1. Запустить контейнеры:
   ```sh
   docker compose up --build
## Описание работы API
### Auth
#### 1. Создание пользователя
- **Метод**: `POST`
- **URL**: `http://localhost:8000/api/v1/auth/register`
- **Тело запроса** (JSON):
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "is_stuff": false,
    "password": "string"
  }
  ```
#### 2. Вход в аккаунт
- **Метод**: `POST`
- **URL**: `http://localhost:8000/api/v1/auth/login`
- **Тело запроса** (JSON):
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
#### 3. Выход из аккаунта
- **Метод**: `DELETE`
- **URL**: `http://localhost:8000/api/v1/auth/logout`

### User
#### 1. Информация о пользователе
- **Метод**: `GET`
- **URL (User)**: `http://localhost:8000/api/v1/user/info`
- **URL (Admin)**: `http://localhost:8000/api/v1/user/info?email=user@example.com`
#### 2. Список пользователей
- **Метод**: `GET`
- **URL**: `http://localhost:8000/api/v1/user/?page=1&size=10`
#### 3. Обновить пользователя
- **Метод**: `PUT`
- **URL**: `http://localhost:8000/api/v1/user/`
- **Тело запроса** (JSON):
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "is_stuff": false,
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
  ```
#### 4. Удалить пользователя
- **Метод**: `DELETE`
- **URL**: `http://localhost:8000/api/v1/user/`
- **Тело запроса** (JSON):
  ```json
  {
    "email": "string"
  }
  ```

### Payment
#### 1. Информация о платежах пользователя
- **Метод**: `GET`
- **URL (User)**: `http://localhost:8000/api/v1/payment/?page=1&size=10`
- **URL (Admin)**: `http://localhost:8000/api/v1/payment/?user_id=<user_id>&page=1&size=10`
#### 2. Создание платежа
- **Метод**: `POST`
- **URL**: `http://localhost:8000/api/v1/payment/webhook`
- **Тело запроса** (JSON):
  ```json
  {
    "transaction_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "amount": 0,
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "signature": "string"
  }
  ```

### Account
#### 1. Информация об счетах пользователя
- **Метод**: `GET`
- **URL (User)**: `http://localhost:8000/api/v1/account/?page=1&size=10`
- **URL (Admin)**: `http://localhost:8000/api/v1/account/?user_id=<user_id>&page=1&size=10`

## Используемые технологии
| Компонент                          | Технология                                    |
|------------------------------------|-----------------------------------------------|
| **Фреймворк для WalletAPI Service**| [FastAPI](https://fastapi.tiangolo.com/)      |
| **База данных**                    | [PostgreSQL](https://www.postgresql.org/)     |
| **Контейнеризация**                | [Docker](https://www.docker.com/)             |
