1. Установка зависимостей: `sudo apt update && sudo apt install -y docker.io docker-compose`
2. Структура проекта была унаследована от предыдущих заданий, в том числе flask приложение
3. Создал файл зависимостей *app/requirements.txt*:
	- flask 
	- psycopg2-binary
4.  Написание `Dockerfile` для Flask (`app/Dockerfile`)
	```
	FROM python:latest
	WORKDIR /app 
	COPY requirements.txt . 
	RUN pip install --no-cache-dir -r requirements.txt 
	COPY app_bd.py .
	EXPOSE 5050
	CMD ["python", "app.py"]```
\
в данном dockerfile собирается образ python с рабочей директорией app, после чего в данную директорию копируется файл зависимостей, далее осуществляется установка данных зависимостей и копирование файла app_bd.py и запуск сервера flask

5. После написания Dockerfile был создан docker-compose: в котором были описаны postgresql и nginx с dockerfile:
	5.1 Postgresql
```
	services:
  db:
    image: postgres:16
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: P@ssw0rd
      POSTGRES_DB: test_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
```

- ports:
	- **"5432:5432"** → Проброс порта 5432 хоста в контейнер (нужен для подключения к БД извне).
- volumes:
	- **pgdata:/var/lib/postgresql/data** → Данные базы будут сохраняться в Docker volume `pgdata`, чтобы не потерять их при перезапуске контейнера.

6. flask_app:
	```
	backend:
	    build: .
	    container_name: flask_app
	    depends_on:
	      - db
	    ports:
	      - "5050:5050"
	```

- **build: .** → Строим образ из текущей директории (нужен `Dockerfile`).
- **depends_on: db** → Запускается только после старта `db`.
- **ports:**
    - **"5050:5050"** → Flask работает на 5050 порту, пробрасываем его наружу.

7 . Nginx
```
  nginx:
    image: nginx:latest
    container_name: nginx
    depends_on:
      - backend
    ports:
      - "80:80"
    volumes:
      - ./default.conf:/etc/nginx/conf.d/default.conf

```

**volumes:**

- **./default.conf:/etc/nginx/conf.d/default.conf** → Подключение конфига Nginx с хоста.
	```
	server {

    listen 80;

    server_name flask.local;

  

    location / {

        proxy_pass http://flask_app:5050/tables;

    }
}


```
volumes:
  pgdata:
```
**pgdata** → Этот volume используется для хранения данных PostgreSQL.

Для запуска необходимо `docker-compose up -d`

Заполнение данных в бд выполнено через `docker exec -it postgres psql -U postgres`