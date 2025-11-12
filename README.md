# Инцидент-трекер

Простой сервис для учёта инцидентов на основе Django и Django Rest Framework.

## Как запустить?

1. Клонируйте репозиторий.
2. Установите зависимости (`pip install -r requirements.txt`).
3. Примените миграции базы данных (`python manage.py migrate`).
4. Запустите сервер разработки (`python manage.py runserver`).

## Эндпоинты

- `/incidents/`: создание нового инцидента, получение списка инцидентов (с поддержкой фильтров по статусу).
- `/incidents/{id}/`: обновление статуса конкретного инцидента.

## Пример запросов:

> Запускать в отдельном окне терминала

### Добавление инцидента

```
# Формирование тела запроса (source = OPERATOR, MONITORING, PARTNER)
$data = @{
    description = "Внимание! Поступил новый инцидент!"
    source = "OPERATOR"
}

# Преобразование в JSON
$body = $data | ConvertTo-Json

# Заголовки
$headers = @{
    "Content-Type" = "application/json; charset=utf-8"
}

# Отправляем запрос
try {
    $response = Invoke-RestMethod `
        -Method POST `
        -Uri 'http://127.0.0.1:8000/incidents/' `
        -Body $body `
        -Headers $headers `
        -ContentType "application/json; charset=utf-8"

    # Выводим каждый элемент отдельно с обработкой UTF-8
    Write-Host "ID: $($response.id)"
    Write-Host "Description: $([Text.Encoding]::UTF8.GetString([byte[]][char[]]$response.description))"
    Write-Host "Source: $([Text.Encoding]::UTF8.GetString([byte[]][char[]]$response.source))"
    Write-Host "Created At: $($response.created_at)"
} catch {
    Write-Host "Ошибка отправки запроса или обработки ответа: $($_.Exception.Message)"
}
```

### Получение списка всех инцидентов

```
# GET-запрос для получения списка инцидентов
$response = Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:8000/incidents/'
# Обработка и вывод результата с явным указанием UTF-8
foreach ($item in $response) {
    Write-Host "ID: $($item.id)" -ForegroundColor Green
    Write-Host "Description: $([Text.Encoding]::UTF8.GetString([byte[]][char[]]$item.description))" -ForegroundColor Yellow
    Write-Host "Source: $([Text.Encoding]::UTF8.GetString([byte[]][char[]]$item.source))" -ForegroundColor Blue
    Write-Host "Status: $($item.status)" -ForegroundColor Magenta
    Write-Host "-------------------------"
}

Получение списка инцидентов с фильтрацией по статусу
# GET-запрос с фильтром по статусу. Status = NEW   IN_PROGRESS   RESOLVED   CLOSED
$response = Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:8000/incidents/?status=IN_PROGRESS'

# Вывод с корректной обработкой UTF-8
foreach ($item in $response) {
    Write-Host "ID: $($item.id)" -ForegroundColor Green
    Write-Host "Description: $([Text.Encoding]::UTF8.GetString([byte[]][char[]]$item.description))" -ForegroundColor Yellow
    Write-Host "Source: $([Text.Encoding]::UTF8.GetString([byte[]][char[]]$item.source))" -ForegroundColor Blue
    Write-Host "Status: $($item.status)" -ForegroundColor Magenta
    Write-Host "-------------------------"
}
```

### Изменение статуса инцидента

```
# ID инцидента, который хочешь обновить
$id = "18"

# Новый статус: NEW   IN_PROGRESS   RESOLVED   CLOSED
$new_status = "RESOLVED"

# Тело запроса
$body = @{
    status = $new_status
} | ConvertTo-Json

# PATCH-запрос для изменения статуса
try {
    $response = Invoke-RestMethod `
        -Method Patch `
        -Uri "http://127.0.0.1:8000/incidents/$id/" `
        -Body $body `
        -ContentType "application/json"

    # Выводим результат
    Write-Host "Статус изменён на: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "Ошибка изменения статуса: $($_.Exception.Response.StatusCode.Value__) $($_.Exception.Message)" -ForegroundColor Red
}
```

---
Это решение легко масштабируется и поддерживает дальнейшее развитие функционала.
