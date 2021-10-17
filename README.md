# v8i-service

Сервис общих информационных баз

## подготовка

```bash
python3 -m pip install --no-cache-dir -r requirements.txt
```

## запуск

```bash
python3 -m uvicorn app.main:app
```

## запуск в docker

перед запуском смонтируйте каталог с файлами *.v8i и укажите его приложению, по умолчанию tests/files

### windows

```cmd
docker run -p 8000:80/tcp -v %CD%/tests/files:/v8i -e V8I_FOLDER="/v8i" korotovskih/v8iservice:0.1.1
```

### linux

```cmd
docker run -p 8000:80/tcp -v $(pwd)/tests/files:/v8i -e V8I_FOLDER="/v8i" korotovskih/v8iservice:0.1.1
```

### проверка

```bash
curl http://localhost:8000/v1/soap/bases/testlist/WebCommonInfoBases
     ^^^^^^^^^^^^^^^^^^^^^               ^^^^^^^^
     локация сервиса APP_HOST            имя вашего файла в каталоге V8I_FOLDER
```

## настройки

app/config.py:

* V8I_FOLDER - публикуемый каталог v8i, каждый файл *.v8i будет опубликован, как отдельный ресурс
* APP_HOST - локация сервиса

### пример

* /v8i/`testlist.v8i`
* `V8I_FOLDER=/v8i`
* `APP_HOST=https://sub.domain.ru/rel/location`

список `testlist.v8i` будет доступен по адресу `https://sub.domain.ru/rel/location/v1/soap/bases/testlist/WebCommonInfoBases`
