1. Установил postgresql из обычного репозитория
2. Создал БД `test_db`
   Создал таблицу командой: `CREATE TABLE data (id SERIAL PRIMARY KEY, data VARCHAR(100));`  и заполнить её тестовыми данными (`insert into data (data) values ('Other Information!');`)
3. Запуск Flask с PostgeSQL: 
	- **Подключение к базе данных**:
    
	    - В функции `get_db_connection` происходит подключение к базе данных PostgreSQL с использованием библиотеки `psycopg2`.
	    - **`функция connect`** содержит строку подключения, которая включает в себя имя пользователя, пароль, хост и имя базы данных.
	- **Маршрут `/data`**:
    
	    - Маршрут `/users` будет обрабатывать GET-запросы.
	    - Внутри маршрута выполняется SQL-запрос для получения всех записей из таблицы `users`.
	    - Результаты запроса (`cur.fetchall()`) преобразуются в список словарей, где каждый словарь содержит данные из строки таблицы.
	    - Ответ возвращается в формате JSON с помощью функции `jsonify`.
	- **Запуск приложения**:
    
	    - В конце файла осуществляется запуск Flask сервера в режиме откладки `app.run(debug=True)`
4. Подключение и натсройка slave-репликации:
	- **Подготовка Master-сервера:**
	
		- Изменил `postgresql.conf:`
			1. listen_addresses = '*' - какие адреса слушает сервер
			2. wal_level = replica - уровень логирования для реплик
			3. max_wal_senders = 10 - максимальное кол-во подлючаемых реплик
		- Добавил разрешение на подключение реплики в `pg_hba.conf`:
			`host replication db_slave 192.168.142.129/32 md5`
		- Создал пользователя для репликации:
		`CREATE ROLE db_slave WITH REPLICATION LOGIN PASSWORD 'P@ssw0rd';`
		- Перезапускаем PostgreSQL на мастере: `sudo systemctl restart postgresql`

	- **Подготовка Slave-сервера:**
		- Необходима остановки службы postgresql
		- Очистка старых данных: `sudo rm -rf /var/lib/postgresql/16/main/*`
		- Скопировал базу с мастера через `pg_basebackup` (Утилита для создания полного бэкапа базы PostgreSQL):
		`pg_basebackup -h 192.168.142.1 -D /var/lib/postgresql/16/main -U db_slave -P --wal-method=stream` (--wal-method=stream, передаёт WAL-файлы в реальном времени)
		- Создал файл `standby.signal` для для перевода сервера в **режим реплики (Standby mode)**.
			Это необходимо, т.к. позволяет:
			✔ **Запускаться в режиме реплики** (а не как обычный сервер).  
			✔ **Получать данные с главного сервера (`Primary`)**.  
			✔ **Автоматически переподключаться** в случае временного разрыва связи.
			> [!Success] 
			> Можно создать автоматически, добави тэг -R в `pg_basebackup
			
		- Изменил конфигурацию `postgresql.conf`:
		`primary_conninfo = 'host=192.168.142.1 port=5432 user=db_slave password=P@ssw0rd'`

		- Перепроверил что каталог `/var/lib/postgresql/16/main` принадлежит postgres:
		```
		sudo chown -R postgres:postgres /var/lib/postgresql/16/main 
		sudo chmod 700 /var/lib/postgresql/16/main
		```
	- **Проверка работы:**
	Запускаем PostgreSQL *на мастере* и выполняем SQL-запрос:
		`SELECT * FROM pg_stat_replication;` отображение записи в таблице о подключенной реплике
	На slave: `SELECT pg_is_in_recovery();` ответ t
 
> [!Warning] Важно
> Версии postgresql реплик и мастера должны быть ***одинаковы!!!***

5.  Настроить удалённое подключение к базе (pg_hba.conf, postgresql.conf).
- Т.к. в pg_hba.conf по умолчанию прописана возможность локального подключения, то изменений не потребовалось
- В postgresql.conf в связи с тем что ранее было прописано прослушивать все адреса, изменять также ничего не пришлось
- Удаленное подключение к бд выполнил с помощью: 
	`psql -h <server_ip> -U postgres -d mydb`