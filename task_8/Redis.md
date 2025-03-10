Установка Redis:
`sudo apt install redis-server -y`

Подключаю Redis сервер к бэкэнд приложению flask
`redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)`

 Функция set_key это маршрут для сохранения данных в Redis
```
@app.route('/set/<key>/<value>')
def set_key(key, value):
    redis_client.set(key, value)
    return jsonify({"message": f"Key {key} set with value {value}."})
```

Этот маршрут позволяет записывать данные в Redis:

- При обращении к `/set/<ключ>/<значение>` Redis сохраняет `ключ: значение`.
- Например, `GET /set/name/DevOps сохранит `name = DevOps`.

Маршрут для получения данных из Redis

```
@app.route('/get/<key>')
def get_key(key):
    value = redis_client.get(key)
    return jsonify({key: value})
```

Этот маршрут позволяет получать данные из Redis:

- При обращении к `/get/<ключ>` сервер возвращает значение ключа.
- Например, `GET /get/name` вернет `{"name": "DevOps"}`.

curl -X GET http://localhost:5000/get/name 

Ответ:
{
  "name": "DevOps"
}