# API для управления расписанием приема лекарств с автоматическим созданием напоминаний и поддержкой бесконечных курсов.

## Основные функции
- Создание курсов лечения с указанием периодичности и длительности
- Автоматическая генерация расписания напоминаний
- Продление расписания для бесконечных курсов
- Получение ближайших приемов лекарств
- Удаление устаревших напоминаний

## Технологии
- Django 
- Django REST Framework
- Celery + Redis
- SQLite

---

## API Endpoints

### `POST /api/schedule/`
Создание нового курса лечения

#### Параметры (JSON):
```json
{
  "name": "Аспирин",
  "user_id": 123,
  "frequency": 8,
  "duration": 7 #необязательный параметр(если даты окончания курса нет)
}
```

#### Ответ:
- `201 Created`: ID созданного курса
- `400 Bad Request`: Ошибки валидации
---

### `GET /api/schedule/`
Получение расписания на ближайшие 24 часа

#### Параметры:
- `user_id` 
- `schedule_id`

#### Ответ:
- `200 OK`: Список напоминаний
- `403 Forbidden`: Несовпадение пользователя
- `404 Not Found`: Объект не найден

---

### `GET /api/schedules/`
Получение всех курсов пользователя

#### Параметры:
- `user_id` (обязательно)

#### Ответ:
- `200 OK`: Список курсов лечения

---

### `GET /api/next_taking/`
Получение приемов в ближайшее время (указывается в .env)

#### Параметры:
- `user_id` (обязательно)

#### Ответ:
- `200 OK`: Список ближайших приемов

---

## ⚙ Запуск проекта

### Требования
- Python 3.9+
- Redis (для Celery)
- Установленные зависимости:
  ```bash
  pip install -r requirements.txt
  ```

### Настройка окружения
1. Создайте файл `.env` в корне проекта:
   ```ini
   SECRET_KEY=ваш_секретный_ключ
   NEXT_TAKKING_HOURS=1 (часы для next_takking)
   ```

2. Выполните миграции:
   ```bash
   python manage.py migrate
   ```

### Запуск сервера
```bash
python manage.py runserver
```

---

## Настройка Celery
Для работы периодических задач требуется запустить Celery Worker и Beat.

### Установка зависимостей
```bash
pip install celery django-celery-beat redis
```

### Запуск Celery
1. **Worker** (в отдельном терминале):
   ```bash
   celery -A your_project.celery worker --loglevel=info
   ```

2. **Beat** (в другом терминале):
   ```bash
   celery -A your_project.celery beat --loglevel=info
   ```


---

## Модели данных
- **CustomUser**: Пользователь системы (только ID)
- **Cure**: Курс лечения
- **Schedule**: Расписание напоминаний

---

## Примеры запросов

**Создание курса лечения:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name":"Аспирин", "user_id":123, "frequency":6, "duration":7}' \
http://localhost:8000/api/schedule/
```

**Получение расписания:**
```bash
curl http://localhost:8000/api/schedule/?user_id=123&schedule_id=1
```

---


