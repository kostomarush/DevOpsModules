 1. Установил Nginx сервер
 2. создал конфиг /etc/nginx/sites-available/app_devops:
 ```
 server { 
	 listen 80; 
	 server_name app1.devops; 
 location /app11/ 
		 { 
	proxy_pass http://127.0.0.1:9999/; 
	
	} 
}
```
за счет чего осуществляется перенаправление с http://app1.devops:80 -> http://127.0.0.1:9999/app11
После чего создал символьную ссылку `sudo ln -s /etc/nginx/sites-available/app_develop /etc/nginx/sites-enabled/` и удалил старую ссылку на конфиг по умолчанию после чего перезагрузил nginx

Аналогичную работу провел с вариантом взаимодействия по другому маршруту

>[! Quote]
>Создал привязку в локальном файле etc для перенаправления запросов app1.devops на указанный адрес.

