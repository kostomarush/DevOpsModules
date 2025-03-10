from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Подключение к Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.route('/set/<key>/<value>')
def set_key(key, value):
    redis_client.set(key, value)
    return jsonify({"message": f"Key {key} set with value {value}."})

@app.route('/get/<key>')
def get_key(key):
    value = redis_client.get(key)
    return jsonify({key: value})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
