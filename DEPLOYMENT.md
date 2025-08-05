# Развертывание на Render.com

## Настройка проекта

1. **Создайте новый Web Service на Render.com**
2. **Подключите ваш GitHub репозиторий**
3. **Настройте переменные окружения:**

### Переменные окружения:
- `SECRET_KEY` - секретный ключ Django (генерируется автоматически)
- `PYTHON_VERSION` - версия Python (3.11.0)

### Настройки сервиса:
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn shopsite.wsgi:application`
- **Environment:** Python

## Файлы для развертывания:

### requirements.txt
Содержит все необходимые зависимости:
- Django==5.2.4
- Pillow==10.1.0 (для работы с изображениями)
- whitenoise==6.6.0 (для статических файлов)
- gunicorn==21.2.0 (WSGI сервер)

### build.sh
Скрипт сборки, который:
- Устанавливает зависимости
- Собирает статические файлы
- Применяет миграции

### render.yaml
Конфигурация для автоматического развертывания

## После развертывания:

1. Создайте суперпользователя через Django Admin
2. Добавьте товары через админ-панель
3. Настройте изображения товаров

## Структура проекта:
```
arish/
├── manage.py
├── requirements.txt
├── build.sh
├── render.yaml
├── shopsite/
│   ├── settings.py
│   ├── settings_production.py
│   └── wsgi.py
├── shop/
├── landing/
└── media/
``` 