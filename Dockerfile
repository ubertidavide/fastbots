FROM python:3.11

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock* .

COPY ./fastbot /fastbot
WORKDIR /fastbot

# Intall only production dependencies
RUN poetry install --no-root --no-dev

CMD ["poetry", "run python main.py"]

