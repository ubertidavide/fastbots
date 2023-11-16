FROM python:3.11

# update dependencies
RUN apt-get update && apt-get upgrade -y 

# install firefox
RUN apt install firefox-esr -y

# install vnc
#RUN apt-get install -y x11vnc xvfb 

# install poetry
RUN curl -sSL https://install.python-poetry.org | python -

COPY pyproject.toml poetry.lock* ./

# Intall only production dependencies
RUN ~/.local/share/pypoetry/venv/bin/poetry install --without dev

COPY . .

#EXPOSE 5900

#Set envirnmental variable for display	
#ENV DISPLAY :20

ENV MOZ_HEADLESS=0
#ENV MOZ_HEADLESS_HEIGHT=2500
#ENV MOZ_HEADLESS_WIDTH=1200

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]