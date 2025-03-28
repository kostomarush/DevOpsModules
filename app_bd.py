import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Подключение к PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="P@ssw0rd",
        host="postgres",
        port="5432"
    )

# Маршрут для получения всех данных из всех таблиц
@app.route('/tables')
def get_all_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM data;")
    tables = cur.fetchall()
    
    cur.close()
    conn.close()
    return jsonify([{"id": t[0], "data": t[1]} for t in tables])

@app.route('/test')
def get_test():
    return "<h1>Kuber v.3</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
