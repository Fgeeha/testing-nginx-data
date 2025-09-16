# 🧪 Testing Nginx Data - Сравнение браузеров

Проект для тестирования данных, которые получает nginx от различных браузеров, и записи этих данных в логи для сравнения.

## 🎯 Назначение

Этот проект позволяет:
- Собирать и анализировать данные запросов от разных браузеров
- Сравнивать поведение различных браузеров (Chrome, Firefox, Safari, Edge)
- Логировать детальную информацию о каждом запросе
- Анализировать производительность и особенности запросов

## 🏗️ Структура проекта

```
testing-nginx-data/
├── nginx.conf              # Кастомная конфигурация nginx
├── docker-compose.yml      # Docker композиция для запуска
├── Dockerfile              # Образ контейнера
├── html/                   # Веб-файлы
│   ├── index.html          # Главная страница для тестирования
│   └── large-file.txt      # Большой файл для тестов производительности
├── scripts/                # Скрипты для тестирования и анализа
│   ├── test-browsers.sh    # Симуляция запросов от разных браузеров
│   └── analyze-logs.py     # Анализ логов nginx
└── logs/                   # Директория для логов (создается автоматически)
```

## 🚀 Быстрый старт

### Требования
- Docker
- Docker Compose
- Python 3 (для анализа логов)

### 1. Запуск сервера

```bash
# Клонировать репозиторий
git clone https://github.com/Fgeeha/testing-nginx-data.git
cd testing-nginx-data

# Запустить nginx сервер
docker compose up -d

# Проверить статус
docker compose ps
```

Сервер будет доступен по адресу: http://localhost:8080

### 2. Тестирование в браузере

1. Откройте http://localhost:8080 в разных браузерах
2. Используйте кнопки тестирования на странице
3. Каждый браузер будет отправлять уникальные данные

### 3. Автоматическое тестирование

```bash
# Симуляция запросов от разных браузеров
./scripts/test-browsers.sh http://localhost:8080

# Анализ логов
./scripts/analyze-logs.py ./logs/browser_access.log --detailed

# Экспорт в JSON
./scripts/analyze-logs.py ./logs/browser_access.log --json report.json
```

## 📊 Что собираем

### Информация о запросах:
- **IP адрес** клиента
- **User-Agent** строка
- **Заголовки Accept** (content types, языки, кодировки)
- **Время выполнения** запроса
- **Размер ответа**
- **HTTP статус коды**
- **Кастомные заголовки**

### Конечные точки тестирования:
- `/` - Главная страница с JavaScript тестами
- `/test/json` - JSON API
- `/test/xml` - XML ответ
- `/test/large` - Большой файл для тестов производительности
- `/api/browser-info` - Сбор информации о браузере

## 🔍 Анализ данных

### Формат логов
Используется кастомный формат логирования nginx:
```
$remote_addr - $remote_user [$time_local] "$request" $status $bytes_sent 
"$http_referer" "$http_user_agent" "$http_accept" "$http_accept_language" 
"$http_accept_encoding" "$http_connection" "$http_cache_control" "$http_dnt" 
"$http_upgrade_insecure_requests" $request_time $upstream_response_time
```

### Скрипт анализа
```bash
# Базовый анализ
python3 scripts/analyze-logs.py logs/browser_access.log

# Детальное сравнение браузеров
python3 scripts/analyze-logs.py logs/browser_access.log --detailed

# Экспорт результатов в JSON
python3 scripts/analyze-logs.py logs/browser_access.log --json browser_report.json
```

## 🌐 Различия между браузерами

### Chrome
- Богатый набор Accept заголовков
- Поддержка современных веб-стандартов
- Агрессивное кэширование

### Firefox
- Уникальный User-Agent формат
- Отличные Accept-Language заголовки
- Строгие политики безопасности

### Safari
- Минималистичные заголовки
- Специфичная обработка WebKit
- Уникальные мобильные характеристики

### Edge
- Сочетание Chrome и уникальных Microsoft заголовков
- Улучшенная безопасность
- Интеграция с Windows

## 📈 Примеры использования

### 1. Тестирование производительности
```bash
# Запустить нагрузочное тестирование
for i in {1..100}; do
    curl -H "User-Agent: Chrome-Test-$i" http://localhost:8080/test/large &
done
wait

# Анализировать результаты
python3 scripts/analyze-logs.py logs/browser_access.log --detailed
```

### 2. A/B тестирование
- Используйте разные браузеры для тестирования одной функциональности
- Сравните времена ответа и поведение
- Анализируйте различия в заголовках

### 3. Мониторинг безопасности
- Отслеживайте подозрительные User-Agent строки
- Анализируйте паттерны запросов
- Выявляйте аномалии в поведении

## 🛠️ Настройка

### Изменение порта
```yaml
# docker-compose.yml
ports:
  - "8081:80"  # Изменить на нужный порт
```

### Кастомизация логирования
Измените формат в `nginx.conf`:
```nginx
log_format custom_format '$remote_addr - [$time_local] "$request" $status';
access_log /var/log/nginx/access.log custom_format;
```

## 🤝 Участие в проекте

1. Форкните репозиторий
2. Создайте ветку для функциональности
3. Внесите изменения
4. Создайте Pull Request

## 📝 Лицензия

MIT License - см. файл LICENSE для деталей.

---

**Автор**: Fgeeha  
**Проект**: Testing Nginx Data  
**Цель**: Сравнение поведения браузеров через анализ nginx логов