# Anthil Project

**Anthil**

## Стек технологий

- **[Flask](https://flask.palletsprojects.com/)** — для создания веб-приложений.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — для работы с базой данных.
- **[Alembic](https://alembic.sqlalchemy.org/)** — для миграций базы данных.
- **[PostgreSQL](https://www.postgresql.org/)** — для хранения данных.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — для работы с переменными окружения.
- **[mypy](http://mypy-lang.org/)** — для статического анализа типов.
- **[ruff](https://github.com/charliermarsh/ruff)** — для линтинга кода.
- **[pytest](https://pytest.org/)** — для написания тестов.

## Установка

Для начала работы с проектом нужно создать виртуальное окружение и установить зависимости.

1. **Создание виртуального окружения**:

    ```bash
    uv venv
    ```

2. **Активировать виртуальное окружение**:

    - Для **Windows (Git Bash)**:
      ```bash
      .venv/Scripts/activate
      ```

    - Для **macOS/Linux**:
      ```bash
      source .venv/bin/activate
      ```

3. **Установка зависимостей**:

    В виртуальном окружении установим все необходимые пакеты:

    ```bash
    uv pip install .[dev]
    ```

    Это установит все зависимости, включая библиотеки для разработки, такие как `flake8`, `pytest`, и другие.

4. **Настройка Alembic**:

    Чтобы управлять миграциями базы данных, выполните следующие шаги:

    - Инициализируйте Alembic:

      ```bash
      alembic init alembic
      ```

    - Настройте строку подключения в `alembic.ini`:

       ```python
       from anthill.config import get_db_url
       config.set_main_option("sqlalchemy.url", get_db_url())
       ```

    - Создайте миграцию с помощью команды:

      ```bash
      alembic revision --autogenerate -m "Initial migration"
      ```

    - Примените миграцию:

      ```bash
      alembic upgrade head
      ```

4. **DLL**:
