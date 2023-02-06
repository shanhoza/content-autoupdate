# Автоматизированная система обновления контента на [сайте](https://modsfortanks.ru/)

## Процесс обновления записей на сайте включает в себя:

- Авторизацию на сайт, сбор информации по записям, которые предстоит обновить.

- Переход на источники записей, первоначальная сверка версий продукта и текущей версии на сайте. Скачивание архивов с источников.

- Повторная сверка версий архивов с текущей версией на сайте. Изменение ссылок в архиве.

- Обновление архива на сайте, обновление текущей версии записи.

## Запуск:

Скопируйте `.env.example` в `.env` и отредактируйте `.env` файл, заполнив в нём все переменные окружения:

```bash
cp content_autoupdate/.env.example content_autoupdate/.env
```

Для управления зависимостями используется [poetry](https://python-poetry.org/),
требуется Python 3.11.

Установка зависимостей и запуск:

```bash
poetry install
poetry run python -m content_autoupdate
```

## Todo:

- Refactor

- Реализовать функционал отправки обновленной информации

- Deploy

# Refactor:

- Отрефачить файлы sources, sources_parsers, download_files, archives, вынести бизнес логику в сервисы, ручки в контроллеры
