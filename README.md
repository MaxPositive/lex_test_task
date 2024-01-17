# Тестовое задание

## 1 задача
### Разработать RESTful сервис с использованием FastAPI и REDIS
#### Endpoints(Эндпоинты)
1. ```POST /addresses``` - в body передается ```phone:str и address: str```
Возвращает сообщение: ```Address written successfully``` и ```status code: 201```.

Если адрес уже существует - возвращает ```status: 409``` и сообщение:
```Address already exists```

2. ``` GET /addresses``` - в ```query параметре``` передается ```phone:str```.
Возвращает ```address:str```.

Если адреса по номеру нету, возвращает ```Address not found``` и ```status code: 404```

3. ``` PUT /addresses``` - в body передается ```phone:str и address: str```
Возвращает сообщение: ```Address updated successfully``` и ```status code: 201```.

Если адреса по номеру нету, возвращает ```Address not found``` и ```status code: 404```

4. ``` DELETE /addresses ``` - в ```query параметре``` передается ```phone:str```.
Возвращает ```status code: 204```

[Создание адреса](images/creation_1.png)

[Создание дубликата](images/creation_duplicate.png)

[Чтение адреса](images/read_address.png)

[Обновление адреса](images/update.png)

[Чтение после обновления](images/read_after_update.png)

[Удаление адреса](images/delete.png)

[Обновление после удаления](images/update_after_delete.png)

[Чтение после удаления](images/read_after_delete.png)

### Запуск
1. клонируем репозиторий - ```https://github.com/MaxPositive/lex_test_task.git```
2. заходим в корневую директорию проекта - ```cd lex_test_task```
3. запускаем через docker - ```docker compose up```

3.1 Если не хотите чтобы занимало терминал - ```docker compose up -d```

Чтобы войти в командную оболочку контейнера api - ```docker exec -it api sh```

Чтобы запустить тесты - ```docker exec api pytest tests```
## 2 задача
## Даны 2 таблицы в СУБД Postgres
[Таблицы](images/tables.png)

Нужно обновить колонку ```status``` в full_names, взяв значения из short_names таблицы 
```минимальным количеством запросов```. Также запрос не должен превышать ```10 минут```


Удалось примерно воссоздать такой пример и оптимальными нашел 2 запроса:

#### 1 запрос
```
-- Update status in full_names based on short_names using a substring match
-- Обновление статуса в полных_именах на основе коротких_имен с помощью совпадения подстрок
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE 
    LEFT(full_names.name, POSITION('.' IN full_names.name) - 1) = short_names.name;
```
#### 2 запрос
```
-- Update status in full_names based on short_names using a regular expression pattern match
-- Обновление статуса в полных_именах на основе коротких_имен с помощью совпадения шаблонов регулярных выражений
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE 
    SUBSTRING(full_names.name FROM 'nazvanie[0-9]+') = short_names.name;
```
