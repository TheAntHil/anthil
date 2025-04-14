# Anthil Project

**Anthil**

## Стек технологий

- **[Flask](https://flask.palletsprojects.com/)** — для создания веб-приложений.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — для работы с базой данных.
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

4. **DLL**:
