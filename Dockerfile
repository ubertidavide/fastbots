FROM python:3.11

# update dependencies
RUN apt-get update && apt-get upgrade -y 

# install firefox
RUN apt install firefox -y

# install vnc
RUN apt-get install -y x11vnc xvfb 

# install poetry
RUN curl -sSL https://install.python-poetry.org | python -

COPY pyproject.toml poetry.lock* .

COPY ./fastbot /fastbot
WORKDIR /fastbot

# Intall only production dependencies
RUN poetry install --no-root --no-dev

CMD ["poetry", "run python main.py"]

