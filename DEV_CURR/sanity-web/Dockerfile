FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    vim \
    gcc \
    gettext \
    default-libmysqlclient-dev \
    postgresql-client libpq-dev \
    sqlite3 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/* \
    
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings", "config.prod", "--insecure"]
