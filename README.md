Простой сервис для регистрации заявок пользователей. Сделан как тестовое задание. Реализован асинхронно.
Помимо основного функционала реализовано логирование в файл и в консоль + настройки логгера через словарь.
Также реализована валидация данных через Pydantic.
Python 3.11 + FastAPI + PostgreSQL 15 + Apache Kafka. Server - uvicorn.
Pytest, Uvicorn. ORM - SQLAlchemy. 
Docker + Docker Compose. 



**Структура:**
* app - корневая папка проекта
*    main.py - точка входа в приложение
*    requirements.txt - файл с зависимостями
*    api/endpoints - здесь лежат первичные обработчики эндпоинтов (см. ниже)
*    core - здесь находятся ключевые элементы сервиса (инициализация приложения, настройки и т.д.)
        - app.py - здесь описана логика инициализации приложения 
        - config.py - здесь описан класс Settings (наследуется от BaseSettings Pydantic) и его взаимодействие с .env
        - database.py - здесь описана логика
           - инициализации базы данных - init_db
           - остановки работы базы данных - stop_db
           - доступа к базе данных (через session) - get_db 
       - kafka.py - здесь описана логика
           - инициализации продюсера Kafka - init_kafka
           - остановки работы продюсера Kafka - stop_kafka
      - settings.env - .env файл, в котором хранятся переменные среды
*    db - здесь находится логика работы с базой данных через ORM - SQLAlchemy
       - base_db_model.py - здесь находится логика инициализации базовой модели SQLAlchemy
       - models - здесь описаны конкретные модели, наследующиеся от базовой
           - application.py - здесь описана модель заявки с помощью класса Application 
       - repositories - здесь описана логика репозиториев для работы с базой данных
           - application_repo.py - репозиторий для заявок - класс ApplicationRepository
*    schemas - здесь описаны схемы для валидации данных с помощью Pydantic
       - application_schema.py - здесь описаны два класса, наследующиеся от BaseModel Pydantic:
           - ApplicationCreate, описывающий необходимые входные данные для создания заявки
           - ApplicationResponse, описывающий данные, необходимые для генерации ответа на запрос на создание заявки
*    utils - здесь описана логика утилитарных инструментов, таких, как логгер
       - logger.py 
         - здесь описана логика логирования в консоль и в файл
         - здесь же находится словарь с настройками логов

* Также в корневой директории находятся:
    - поддиректория с докер-файлом
    - файл docker-compose
    - данный файл с документацией


**Эндпоинты:** 
* '/' - базовый эндпоинт (тестовый) - показывает, что сервер запущен и работает. Ничего не принимает.
     Возвращает строку с приветствием.
* '/applications':
*    с методом POST - принимает два параметра в виде словаря:
        - user_name - имя пользователя
        - description - описание заявки

*    Проверять: через Postman
     - метод POST
     - адрес http://localhost:8000/applications
     - headers:
     - Content-Type: application/json
     - Остальные оставить дефолтные
     - Body (вариант raw, JSON) (пример):  
     - {
        "user_name": "Ilyas_Apunov",
        "description": "Need administrative access"
     }
*    Ожидаемые возвращаемые данные (для данного примера):
-    {
          "id": 1,
          "user_name": "Ilyas_Apunov",
          "description": "Need administrative access",
          "created_at": "2025-01-17 17:34:54.611089"}
*    с методом GET - через query принимает параметры:
        - user_name - имя пользователя
        - количество заявок на странице (опционально)
        - номер страницы (опционально)
        возвращает список заявок (пагинация и фильтрация по имени пользователя реализованы).
    Пример запроса для localhost через браузер:
- http://localhost:8000/applications?size=5&page=1
    Пример возвращаемых данных:
*                {
                    "created_at": "2025-01-17T17:49:50.634683",
                    "user_name": "Ilyas_Apunov",
                    "id": 6,
                    "description": "Need administrative access"
                },
*                {
                    "created_at": "2025-01-17T17:49:51.165685",
                    "user_name": "Ilyas_Apunov",
                    "id": 7,
                    "description": "Need administrative access"
                },
     
    Для проверки пагинации можно 10-12 раз отправить одинаковый POST запрос
    (имя пользователя и содержание заявки не обязаны быть уникальными).


* **Инструкция по запуску:** 
Из корневой папки (FastAPI_App_Demo) запустить команду docker-compose up
(можно в detached режиме) 
Порты указаны в файле docker-compose