1. Создал поточное flask приложение. Установил необходимые зависимости, проверил работоспособность: `source activate env/bin/activate python3 app.py`
2. Написал systemd-юнит с перенаправлением логов
3. Создал пользователя app `sudo adduser`
4. Создал директорию /var/log/flaskapp и файлы логирования flaskapp.log flaskapp-error.log с присвоением прав пользователю app `sudo chown -R app flaskapp/` на все содержимое 
5. Запусти службу `sudo systemctl start flask.service` и установил запуск при загрузке ОС `sudo systemctl enable flask.service`
