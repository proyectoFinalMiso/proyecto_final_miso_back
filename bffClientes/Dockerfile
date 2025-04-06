FROM python:3.12-bookworm

WORKDIR /

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system

RUN pipenv sync

COPY . .

EXPOSE 3096

CMD [ "pipenv", "run", "python", "app.py", "production"]
