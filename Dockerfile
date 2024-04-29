FROM python:3.11

WORKDIR /Elias

ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry install --no-root

COPY src .

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","8000"]

